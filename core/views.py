from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Association, Particulier, Contact, Reclamation
from campaign.models import Campaign
from donation.models import ObjectDonation


# Create your views here.
def homepage(request):
    if request.user.is_authenticated and request.user.is_superuser:
        campaigns = Campaign.objects.filter(status="encours", urgent=False)
    else:
        campaigns = Campaign.objects.filter(status="encours", urgent=False)
    urgents = Campaign.objects.filter(status="encours", urgent=True)
    donations = ObjectDonation.objects.filter(active=True)
    context = {
        "campaigns": campaigns,
        "urgents": urgents,
        "donations": donations
    }
    return render(request, 'index.html', context)


class AnnoncePageView(TemplateView):
    template_name = 'annonce.html'


class CagnottePageView(TemplateView):
    template_name = 'cagnotte.html'


class ErrorPageView(TemplateView):
    template_name = 'error-404.html'


class CguPageView(TemplateView):
    template_name = "cgu.html"


class HowWorkPageView(TemplateView):
    template_name = "how_it_work.html"


class FaqPageView(TemplateView):
    template_name = "faq.html"


class GarantieSecuritePageView(TemplateView):
    template_name = "garantie_securite.html"


class MentionLegalePageView(TemplateView):
    template_name = "mention_legale.html"


class TarifsPageView(TemplateView):
    template_name = "tarifs.html"

class SommesNousPageView(TemplateView):
    template_name = "qui_sommes_nous.html"

class ReclamationPageView(TemplateView):
    template_name = "reclamation.html"


def logout_view(request):
    logout(request)
    return redirect("index")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authentifier l'utilisateur (email ou numéro de téléphone)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect('index')  # Redirigez vers votre page d'accueil ou une autre URL
        else:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")

    return render(request, 'account/login.html')


def register_view(request):
    if request.method == "POST":
        # Récupérer les données POST
        user_type = request.POST.get("user_type")  # "association" ou "particulier"
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        nomassoc = request.POST.get("nomassoc")  # Peut être vide si "Particulier" est choisi
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        try:
            if email is None or phone is None:
                messages.error(request, "Veuillez fournir un email et/ou un numéro de téléphone.")
                return render(request, "account/register.html")

            if user_type == "association" and not nomassoc:
                messages.error(request, "Veuillez fournir le nom de l'association.")
                return render(request, "account/register.html")

            # Valider et traiter les données
            if password != confirmpassword:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return render(request, "account/register.html")

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Un compte avec cet email existe déjà.")
                return render(request, "account/register.html")

            if CustomUser.objects.filter(phone=phone).exists():
                messages.error(request, "Un compte avec ce numéro de téléphone existe déjà.")
                return render(request, "account/register.html")

            user = CustomUser.objects.create(email=email, phone=phone, first_name=firstname, last_name=lastname)
            user.set_password(password)
            user.save()

            if user_type == "association":
                # Logique pour créer une association
                Association.objects.create(user=user, nom_association=nomassoc)
                print(f"Créer un compte pour l'association : {nomassoc}")
            elif user_type == "particulier":
                # Logique pour créer un particulier
                Particulier.objects.create(user=user)
                print(f"Créer un compte pour le particulier : {firstname} {lastname}")

            # Authentifier et connecter l'utilisateur
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect("index")

        except Exception as e:

            return render(request, "account/register.html")

    return render(request, "account/register.html")


def campaing_donation_list(request):
    donations = ObjectDonation.objects.filter(active=True)
    campaigns = Campaign.objects.filter(status="encours")
    context = {
        "donations": donations,
        "campaigns": campaigns
    }
    return render(request, 'campaing_announce.html', context)


def contact_view(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        message = request.POST.get("message")
        # Validation simple
        if nom and email and message:
            # Sauvegarde dans le modèle Contact
            Contact.objects.create(nom_complet=nom, email=email, description=message)
            messages.success(request, "Votre message a bien été envoyé !")
            return redirect(request.path)
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    return render(request, "default.html")


def reclamation_view(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        url_cagnotte = request.POST.get("url_cagnotte")
        connaissance_organisateur = request.POST.get("connaissance_organisateur")
        inquietude = request.POST.get("inquietude")
        description = request.POST.get("description")
        certif_exactitude = request.POST.get("certif_exactitude")
        piece_jointe = request.FILES.get("piece_jointe")

        # Validation simple
        if not all([nom, email, telephone, url_cagnotte, connaissance_organisateur, inquietude, description, certif_exactitude]):
            messages.error(request, "Veuillez remplir tous les champs obligatoires et certifier l'exactitude des informations.")
        else:
            reclamation = Reclamation(
                nom=nom,
                email=email,
                telephone=telephone,
                url_cagnotte=url_cagnotte,
                connaissance_organisateur=connaissance_organisateur,
                inquietude=inquietude,
                description=description,
                certif_exactitude=True if certif_exactitude else False,
                piece_jointe=piece_jointe
            )
            reclamation.save()
            messages.success(request, "Votre réclamation a bien été envoyée. Merci pour votre vigilance !")
            return redirect(request.path)
    return render(request, "reclamation.html")