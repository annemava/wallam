from django.urls import path
from .views import *

urlpatterns = [
    path('announce', announce, name='announce'),
    path('donation/<int:pk>/', donation_detail_view, name='donation_detail'),
]
