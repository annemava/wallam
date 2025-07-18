from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from core.models import Personne
from .models import Campaign, Category, Donation


def create_campaign_view(request):
    categories = Category.objects.filter(active=True)
    if request.method == "POST":
        # Récupérer les données du formulaire
        title = request.POST.get("title")
        beneficiary = request.POST.get("beneficiary")
        beneficiary_phone = request.POST.get("beneficiary_phone")
        goal = request.POST.get("goal")
        duration = request.POST.get("duration")
        code = request.POST.get("code")
        category_id = request.POST.get("category")
        description = request.POST.get("description")
        reward = request.POST.get("reward")
        uploaded_files = request.FILES.get("uploaded_files")
        visibility = request.POST.get("visibility")
        terms_accepted = request.POST.get("terms_accepted") == "on"

        # Validation
        if not terms_accepted:
            messages.error(request, "Vous devez accepter les conditions générales d'utilisation.")
            return redirect("create_campaign")

        if category_id:
            category = Category.objects.get(pk=int(category_id))

        try:
            # Créer la campagne
            campaign = Campaign.objects.create(
                user=request.user,
                title=title,
                beneficiary=beneficiary,
                beneficiary_phone=beneficiary_phone,
                goal=goal if goal else None,
                duration=duration,
                code=code if code else None,
                category=category,
                description=description,
                reward=reward if reward else None,
                uploaded_files=uploaded_files if uploaded_files else None,
                visibility=visibility,
                terms_accepted=terms_accepted,
            )
            return redirect("campaign_detail", pk=campaign.pk)  # Redirige vers la page de détail
        except Exception as e:
            print("erreur ", str(e))
            messages.error(request, f"Erreur lors de la création de la campagne : {str(e)}")
            return redirect("create_campaign")
    context = {
        "categories": categories
    }

    return render(request, "campaign/create_campaign.html", context)


@login_required
def edit_campaign_view(request, pk):
    # Récupérer la campagne existante
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)  # Vérifie que la campagne appartient à l'utilisateur connecté
    categories = Category.objects.filter(active=True).exclude(pk=campaign.category.pk)
    if request.method == "POST":
        # Récupérer les données du formulaire
        title = request.POST.get("title")
        beneficiary = request.POST.get("beneficiary")
        beneficiary_phone = request.POST.get("beneficiary_phone")
        goal = request.POST.get("goal")
        duration = request.POST.get("duration")
        code = request.POST.get("code")
        category = request.POST.get("category")
        description = request.POST.get("description")
        reward = request.POST.get("reward")
        uploaded_files = request.FILES.get("uploaded_files")
        visibility = request.POST.get("visibility")
        terms_accepted = request.POST.get("terms_accepted") == "on"

        # Validation
        if not terms_accepted:
            messages.error(request, "Vous devez accepter les conditions générales d'utilisation.")
            return redirect("edit_campaign", pk=pk)

        try:
            # Mettre à jour la campagne
            campaign.title = title
            campaign.beneficiary = beneficiary
            campaign.beneficiary_phone = beneficiary_phone
            campaign.goal = goal if goal else None
            campaign.duration = duration
            campaign.code = code if code else None
            if category:
                category = Category.objects.get(pk=int(category))
            campaign.category = category
            campaign.description = description
            campaign.reward = reward if reward else None
            if uploaded_files:  # Vérifie si un nouveau fichier est téléchargé
                campaign.uploaded_files = uploaded_files
            campaign.visibility = visibility
            campaign.terms_accepted = terms_accepted
            campaign.save()

            messages.success(request, "La campagne a été mise à jour avec succès.")
            return redirect("campaign_detail", pk=campaign.pk)  # Redirige vers la page de détail
        except Exception as e:
            print("erreur ", e)
            messages.error(request, f"Erreur lors de la modification de la campagne : {str(e)}")
            return redirect("edit_campaign", pk=pk)

    # Préremplir le formulaire avec les données existantes
    context = {
        "campaign": campaign,
        "categories": categories
    }
    return render(request, "campaign/edit_campaign.html", context)

@login_required
def campaign_detail_view(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    context = {
        "campaign": campaign
    }
    return render(request, "campaign/detail_campaign.html", context)


"""from datetime import timedelta

expiration_date = campaign.created_at + timedelta(days=campaign.duration)
is_expired = expiration_date < timezone.now()"""


def campaign_donate(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    context = {
        "campaign": campaign
    }
    if request.method == "POST":
        donor_fullname = request.POST.get("donor_fullname")
        amount = request.POST.get("amount")
        donor_phone = request.POST.get("donor_phone")

        try:
            if donor_fullname:
                Donation.objects.create(campaign=campaign, amount=amount, donor_fullname=donor_fullname,
                                        donor_phone=donor_phone)
            else:
                Donation.objects.create(campaign=campaign, amount=amount, user=request.user,
                                        donor_phone=donor_phone)
            context["amount"] = amount
            return render(request, "campaign/detail_campaign.html", context)
        except Exception as ex:
            print("erreur ", ex)
            return render(request, "campaign/detail_campaign.html", context)

    return render(request, "campaign/campaign_donation.html", context)


def campaign_list(request):
    pass