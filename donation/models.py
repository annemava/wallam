from django.db import models
from core.models import CustomUser as User


class CategoryChoices(models.Model):
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class AvailabilityChoices(models.Model):
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class ConditionChoices(models.Model):
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


# Create your models here.
class ObjectDonation(models.Model):
    # Champs principaux
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=255)  # Localisation du retrait
    category = models.ForeignKey(CategoryChoices, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    availability = models.ForeignKey(AvailabilityChoices, on_delete=models.CASCADE)
    condition = models.ForeignKey(ConditionChoices, on_delete=models.CASCADE)
    expiration_date = models.DateField(blank=True, null=True, help_text="Applicable uniquement pour la nourriture")
    terms_accepted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.category.title}"


class PhotoObject(models.Model):
    object = models.ForeignKey(ObjectDonation, on_delete=models.CASCADE)
    photos = models.ImageField(upload_to="donation_photos/", blank=True, null=True)
