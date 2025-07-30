from django.db import models
from datetime import timedelta, date
from core.models import CustomUser as User
from django.templatetags.static import static


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

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
    urgent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def days_remaining(self):
        """
        Retourne le nombre de jours restants pour la campagne.
        Si la campagne est terminée, retourne 0.
        """
        end_date = self.created_at.date() + timedelta(days=self.duration)
        remaining_days = (end_date - date.today()).days
        return max(remaining_days, 0)  # Retourne 0 si la date est passée

    def amount_collected(self):
        """
        Retourne la somme totale des contributions pour cette campagne.
        Si aucune contribution n'existe, retourne 0.
        """
        total_contributions = self.donations.aggregate(total=models.Sum('amount'))['total'] or 0
        return total_contributions

    def percentage_collected(self):
        """
        Retourne le pourcentage du montant déjà collecté par rapport à l'objectif.
        Si l'objectif (goal) n'est pas défini, retourne None.
        """
        if self.goal is None or self.goal <= 0:
            return None

        total_contributions = self.donations.aggregate(total=models.Sum('amount'))['total'] or 0
        percentage = (total_contributions / self.goal) * 100
        return round(min(percentage, 100), 2)  # Limite à 100% et arrondi à 2 décimales

    def get_image_url(self):

        if self.uploaded_files and self.uploaded_files.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return self.uploaded_files.url

        if self.category:
            base_path = f"images/urgent-slider/{self.category.name.lower()}"
            for ext in ['jpg', 'jpeg', 'png', 'webp', 'PNG', 'JPG', 'JPEG']:
                return static(f"{base_path}.{ext}")  # Choisit la première extension trouvée dans l'ordre (non idéal sans test réel)

        return static("images/urgent-slider/default.jpg")



class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="donations")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="donations")
    donor_fullname = models.CharField(max_length=255, blank=True, null=True)  # Pour les donateurs non inscrits
    donor_phone = models.CharField(max_length=255, blank=True, null=True)  # Facultatif pour les donateurs non inscrits
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Don de {self.amount} pour {self.campaign.title}"

