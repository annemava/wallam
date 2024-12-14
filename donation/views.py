from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView
from django.contrib import messages
from .models import Campaign, Donation, ObjectDonation
from .forms import DonationForm, ObjectDonationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def donate_view(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.campaign = campaign
            donation.save()
            messages.success(request, "Merci pour votre don généreux!")
            return redirect('campaign_detail', pk=campaign.pk)
    else:
        form = DonationForm()

    return render(request, 'donate.html', {'form': form, 'campaign': campaign})

@login_required
def donate_object_view(request):
    if request.method == 'POST':
        form = ObjectDonationForm(request.POST, request.FILES)
        if form.is_valid():
            object_donation = form.save(commit=False)
            object_donation.user = request.user
            object_donation.save()
            messages.success(request, "Merci pour votre don généreux!")
            return redirect('donation_list')
    else:
        form = ObjectDonationForm()

    return render(request, 'object_donation_form.html', {'form': form})


class DonateView(FormView):
    template_name = "donate.html"
    form_class = DonationForm

    def form_valid(self, form):
        campaign_id = self.kwargs.get('pk')
        campaign = get_object_or_404(Campaign, pk=campaign_id)

        # Créer le don
        donation = form.save(commit=False)
        donation.campaign = campaign

        if self.request.user.is_authenticated:
            donation.user = self.request.user
        elif not form.cleaned_data['donor_name'] or not form.cleaned_data['donor_email']:
            # Si non inscrit, le nom et l'email sont obligatoires
            messages.error(self.request, "Nom et email sont requis pour un don sans inscription.")
            return self.form_invalid(form)

        donation.save()

        # Message de succès
        messages.success(self.request, "Merci pour votre don généreux!")
        return redirect('campaign_detail', pk=campaign.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaign'] = get_object_or_404(Campaign, pk=self.kwargs.get('pk'))
        return context


class ObjectDonationCreateView(CreateView):
    model = ObjectDonation
    form_class = ObjectDonationForm
    template_name = "object_donation_form.html"
    success_url = reverse_lazy('donation_list')  # Remplacez par l'URL de votre liste des dons

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associe l'annonce à l'utilisateur connecté
        photos = self.request.FILES.getlist('photos')
        if len(photos) > 3:
            messages.error(self.request, "Vous ne pouvez télécharger que 3 photos au maximum.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire.")
        return super().form_invalid(form)
