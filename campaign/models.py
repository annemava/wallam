from django.db import models
from core.models import CustomUser as User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Publique'),
        ('private', 'Privée'),
    ]

    STATUS_CHOICES = [
        ('encours', 'Encours'),
        ('terminee', 'Terminee'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="campaigns")  # L'utilisateur qui crée la campagne
    title = models.CharField(max_length=255)
    beneficiary = models.CharField(max_length=255)
    beneficiary_phone = models.CharField(max_length=15)
    goal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration = models.IntegerField(help_text="Durée en jours")
    code = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category,  on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    reward = models.TextField(blank=True, null=True)
    uploaded_files = models.FileField(upload_to="campaign_files/", blank=True, null=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    terms_accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='encours')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

