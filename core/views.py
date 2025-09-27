from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Association, Particulier, Contact, Reclamation, Conversation, Message
from campaign.models import Campaign, Donation
from donation.models import ObjectDonation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.
def homepage(request):
    if request.user.is_authenticated and request.user.is_superuser:
        campaigns = Campaign.objects.filter(status="encours", urgent=False)
    else:
        campaigns = Campaign.objects.filter(status="encours", urgent=False, visibility="public")
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
        next_url = request.POST.get("next") or request.path
        # Validation simple
        if nom and email and message:
            # Sauvegarde dans le modèle Contact
            Contact.objects.create(nom_complet=nom, email=email, description=message)
            messages.success(request, "Votre message a bien été envoyé !")
            print("request.path ", next_url)
            return redirect(next_url)
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect(next_url)
    return redirect("index")


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
            return redirect("index")
    return redirect("index")


@login_required
def conversations_list(request):
    try:
        particulier = Particulier.objects.get(user=request.user)
    except Particulier.DoesNotExist:
        return redirect("index")
    conversations = particulier.conversations.all()
    return render(request, "messagerie/conversations_list.html", {"conversations": conversations})

@login_required
def conversation_detail(request, conversation_id):
    try:
        particulier = Particulier.objects.get(user=request.user)
    except Particulier.DoesNotExist:
        return redirect("index")
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=particulier)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(conversation=conversation, sender=particulier, content=content)
        return redirect("conversation_detail", conversation_id=conversation.id)
    messages_list = conversation.messages.all()
    return render(request, "messagerie/conversation_detail.html", {"conversation": conversation, "messages": messages_list})


def start_conversation(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    # user_id est l'id du CustomUser cible
    other_user = get_object_or_404(CustomUser, pk=pk)
    try:
        me = Particulier.objects.get(user=request.user)
        other_particulier = Particulier.objects.get(user=other_user)
    except Particulier.DoesNotExist:
        return redirect("conversations_list")
    # Vérifier si une conversation existe déjà
    conversation = Conversation.objects.filter(participants=me).filter(participants=other_particulier).first()
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(me, other_particulier)
    return redirect("conversation_detail", conversation_id=conversation.id)

def password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[user.pk, token])
            )
            send_mail(
                "Réinitialisation de votre mot de passe",
                f"Pour réinitialiser votre mot de passe, cliquez sur ce lien : {reset_url}",
                "no-reply@wallam.com",
                [email],
            )
            messages.success(request, "Un email de réinitialisation a été envoyé si l'adresse existe.")
        except User.DoesNotExist:
            messages.error(request, "Aucun utilisateur avec cet email.")
    return render(request, "account/forgot.html")

def password_reset_confirm_view(request, uid, token):
    User = get_user_model()
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            user.set_password(new_password)
            user.save()
            messages.success(request, "Mot de passe réinitialisé avec succès.")
            return redirect("login")
        return render(request, "account/reset_confirm.html", {"valid": True})
    else:
        messages.error(request, "Lien invalide ou expiré.")
        return render(request, "account/reset_confirm.html", {"valid": False})

@csrf_exempt
def payment_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_id = data.get("paymentId")
        phone = data.get("phoneNumber")
        status = data.get("status")
        # Retrouve le don correspondant
        donation = Donation.objects.filter(donor_phone=phone).last()
        if donation and status == "SUCCESS":
            pass
            """donation.payment_status = "SUCCESS"
            donation.payment_id = payment_id
            donation.save()"""
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid request"}, status=400)
