from django.shortcuts import render, get_object_or_404, redirect
from .models import *


def announce(request):
    conditions = ConditionChoices.objects.filter(active=True)
    availabilities = AvailabilityChoices.objects.filter(active=True)
    categories = CategoryChoices.objects.filter(active=True)
    context = {
        "conditions": conditions,
        "availabilities": availabilities,
        "categories": categories
    }
    return render(request, 'donation/annonce.html', context)


def donation_detail_view(request, pk):
    donation = get_object_or_404(ObjectDonation, pk=pk)
    context = {
        "donation": donation
    }
    return render(request, "donation/donation_details.html", context)
