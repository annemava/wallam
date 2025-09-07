from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    username = None  # Supprime le champ `username` par défaut
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Personne(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pseudo = models.CharField(max_length=100, null=True, blank=True)
    accept_cgu = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Association(Personne):
    nom_association = models.CharField(max_length=255)
    num_enregistrement = models.CharField(max_length=50, null=True, blank=True)
    type_association = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    document_justificatif = models.FileField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return self.nom_association


class Particulier(Personne):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.email


class Contact(models.Model):
    nom_complet = models.CharField(max_length=255)
    email = models.EmailField(max_length=250, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom_complet

class Reclamation(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=30)
    url_cagnotte = models.URLField()
    connaissance_organisateur = models.CharField(max_length=255)
    inquietude = models.CharField(max_length=255)
    description = models.TextField()
    piece_jointe = models.FileField(upload_to='reclamations/', blank=True, null=True)
    certif_exactitude = models.BooleanField(default=False)
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réclamation de {self.nom} ({self.email})"