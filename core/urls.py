from django.urls import path
from core.views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('annonce', AnnoncePageView.as_view(), name='annonce'),
    path('cagnotte', CagnottePageView.as_view(), name='cagnotte'),
]
