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


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('ASSOCIATION', 'Association'),
        ('PARTICULIER', 'Particulier'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    association = models.CharField(max_length=255, blank=True, null=True)  # Pour les associations
    cgu_validation = models.BooleanField(default=False)  # Pour les particuliers et les associations

    def __str__(self):
        return f"{self.user.email} - {self.get_user_type_display()}"
