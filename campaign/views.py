from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import Campaign


@login_required
def create_campaign_view(request):
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
            return redirect("create_campaign")

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
            messages.success(request, "La campagne a été créée avec succès.")
            return redirect("campaign_detail", pk=campaign.pk)  # Redirige vers la page de détail
        except Exception as e:
            messages.error(request, f"Erreur lors de la création de la campagne : {str(e)}")
            return redirect("create_campaign")

    return render(request, "campaign/create_campaign.html")


@login_required
def edit_campaign_view(request, pk):
    # Récupérer la campagne existante
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)  # Vérifie que la campagne appartient à l'utilisateur connecté

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
            campaign.category = category
            campaign.description = description
            campaign.reward = reward if reward else None
            if uploaded_files:  # Vérifie si un nouveau fichier est téléchargé
                campaign.uploaded_files = uploaded_files
            campaign.visibility = visibility
            campaign.terms_accepted = terms_accepted
            campaign.save()

            messages.success(request, "La campagne a été mise à jour avec succès.")
            return redirect("campaign_detail", pk=campaign.pk)
        except Exception as e:
            messages.error(request, f"Erreur lors de la modification de la campagne : {str(e)}")
            return redirect("edit_campaign", pk=pk)

    # Préremplir le formulaire avec les données existantes
    context = {
        "campaign": campaign,
    }
    return render(request, "campaign/edit_campaign.html", context)

@login_required
def campaign_detail_view(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    context = {
        "campaign": campaign,
    }
    return render(request, "campaign/campaign_detail.html", context)


"""from datetime import timedelta

expiration_date = campaign.created_at + timedelta(days=campaign.duration)
is_expired = expiration_date < timezone.now()"""
