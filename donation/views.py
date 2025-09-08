from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


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

        def resize_image(uploaded_file):
            if uploaded_file:
                try:
                    image = Image.open(uploaded_file)
                    image = image.convert("RGB")
                    image = image.resize((270, 325), Image.Resampling.LANCZOS)
                    buffer = BytesIO()
                    image.save(buffer, format='JPEG')
                    return ContentFile(buffer.getvalue(), name=uploaded_file.name)
                except Exception:
                    return uploaded_file
            return None

        image1 = resize_image(request.FILES.get("image1"))
        image2 = resize_image(request.FILES.get("image2"))
        image3 = resize_image(request.FILES.get("image3"))

        terms_accepted = accepted == "on"

        category = CategoryChoices.objects.get(pk=int(category_id)) if category_id else None
        availability = AvailabilityChoices.objects.get(pk=int(availability_id)) if availability_id else None
        condition = ConditionChoices.objects.get(pk=int(condition_id)) if condition_id else None

        donation_kwargs = {
            "user": request.user,
            "title": title,
            "location": location,
            "category": category,
            "description": description,
            "availability": availability,
            "condition": condition,
            "terms_accepted": terms_accepted,
            "image1": image1,
            "image2": image2,
            "image3": image3,
        }
        if expiration_date:
            donation_kwargs["expiration_date"] = expiration_date

        donation = ObjectDonation.objects.create(**donation_kwargs)
        return redirect("donation_detail", pk=donation.pk)

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