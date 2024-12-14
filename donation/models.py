from django.db import models
from core.models import CustomUser as User
from campaign.models import Campaign


# Create your models here.
class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="donations")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="donations")
    donor_fullname = models.CharField(max_length=255, blank=True, null=True)  # Pour les donateurs non inscrits
    donor_phone = models.CharField(max_length=255, blank=True, null=True)  # Facultatif pour les donateurs non inscrits
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Don de {self.amount} pour {self.campaign.title}"


class ObjectDonation(models.Model):
    # Constantes pour les choix
    CATEGORY_CHOICES = [
        ('object', 'Objet'),
        ('food', 'Nourriture'),
    ]
    AVAILABILITY_CHOICES = [
        ('weekdays', 'Journée en semaine'),
        ('weekend', 'Weekend'),
        ('flexible', 'Flexible'),
    ]
    CONDITION_CHOICES = [
        ('like_new', 'Comme neuf'),
        ('good', 'Bon état'),
        ('average', 'État moyen'),
        ('to_repair', 'À bricoler'),
    ]

    # Champs principaux
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    photos = models.ImageField(upload_to="donation_photos/", blank=True, null=True)
    location = models.CharField(max_length=255)  # Localisation du retrait
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    expiration_date = models.DateField(blank=True, null=True, help_text="Applicable uniquement pour la nourriture")
    terms_accepted = models.BooleanField(default=False)

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"
