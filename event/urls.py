from django.urls import path
from .views import EventPageView

urlpatterns = [
    path('evenement', EventPageView.as_view(), name='event'),
]
