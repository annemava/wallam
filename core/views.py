from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'


class AnnoncePageView(TemplateView):
    template_name = 'annonce.html'


class CagnottePageView(TemplateView):
    template_name = 'cagnotte.html'
