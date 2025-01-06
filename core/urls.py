from django.urls import path
from core.views import *

urlpatterns = [
    path('', homepage, name='index'),
    path('annonce', AnnoncePageView.as_view(), name='annonce'),
    path('cagnotte', CagnottePageView.as_view(), name='cagnotte'),
    path('404', ErrorPageView.as_view(), name='404'),
]
