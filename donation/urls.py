from django.urls import path
from .views import DonateView

urlpatterns = [
    path('campaign/<int:pk>/donate/', DonateView.as_view(), name='campaign_donate'),
]
