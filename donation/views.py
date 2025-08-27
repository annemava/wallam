from django.shortcuts import render, get_object_or_404, redirect
from .models import *


def announce(request):
    if request.method == "POST":
        location = request.POST.get("location")
        category_id = request.POST.get("category")
        availability_id = request.POST.get("availability")
        condition_id = request.POST.get("condition")
        title = request.POST.get("title")
        description = request.POST.get("description")
        expiration_date = request.POST.get("expiration_date")
        accepted = request.POST.get("terms_accepted")

        if accepted == "on":
            terms_accepted = True
        else:
            terms_accepted = False

        if category_id:
            category = CategoryChoices.objects.get(pk=int(category_id))
        if availability_id:
            availability = AvailabilityChoices.objects.get(pk=int(availability_id))
        if condition_id:
            condition = ConditionChoices.objects.get(pk=int(condition_id))
        if expiration_date:
            # Créer la donation d'objet ou de nourriture
            donation = ObjectDonation.objects.create(
                user=request.user,
                title=title,
                location=location,
                category=category,
                description=description,
                availability=availability,
                condition=condition,
                expiration_date=expiration_date,
                terms_accepted=terms_accepted
            )
        else:
            donation = ObjectDonation.objects.create(
                user=request.user,
                title=title,
                location=location,
                category=category,
                description=description,
                availability=availability,
                condition=condition,
                terms_accepted=terms_accepted
            )
        return redirect("donation_detail", pk=donation.pk)  # Redirige vers la page de détail

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


def donation_list(request):
    donations = ObjectDonation.objects.filter(active=True)
    context = {
        "donations": donations
    }
    return render(request, 'donation/list.html', context)