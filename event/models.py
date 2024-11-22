from django.db import models
from django.db.models import Count, Sum
from core.models import CustomUser as User


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)  # Visibilité publique ou privée de l'événement
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_total_tickets_sold(self):
        """Retourne le nombre total de billets vendus pour cet événement."""
        return self.tickets.count()

    def get_total_revenue(self):
        """Retourne le montant total généré par la vente des billets de cet événement."""
        return self.tickets.aggregate(total_revenue=Sum('ticket_type__price'))['total_revenue'] or 0


class TicketType(models.Model):
    event = models.ForeignKey(Event, related_name="ticket_types", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Ex : "VIP", "Standard", "Gratuit"
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Prix du billet
    quantity = models.PositiveIntegerField()  # Quantité de billets disponibles
    is_available = models.BooleanField(default=True)  # Si le billet est encore disponible
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ticket_type = models.ForeignKey(TicketType, related_name="tickets", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="tickets", on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_scanned = models.BooleanField(default=False)  # Si le billet a été scanné à l'entrée
    status = models.CharField(max_length=50, default="Pending")  # Status de paiement (e.g., "Paid", "Pending")

    def __str__(self):
        return f"Ticket {self.id} - {self.event.title}"
