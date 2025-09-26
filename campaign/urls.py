from django.urls import path
from . import views

urlpatterns = [
    path("campaign/create-campaign/", views.create_campaign_view, name="create_campaign"),
    path("campaign/edit-campaign/<int:pk>/", views.edit_campaign_view, name="edit_campaign"),
    path("campaign/<int:pk>/", views.campaign_detail_view, name="campaign_detail"),
    path("campaign/<int:pk>/donate/", views.campaign_donate, name="campaign_donate"),
    path("campaigns", views.campaign_list, name="campaign_list")
]
