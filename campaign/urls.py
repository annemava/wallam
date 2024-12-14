from django.urls import path
from .views import create_campaign_view, edit_campaign_view, campaign_detail_view

urlpatterns = [
    path("create-campaign/", create_campaign_view, name="create_campaign"),
    path("edit-campaign/<int:pk>/", edit_campaign_view, name="edit_campaign"),
    path("campaign/<int:pk>/", campaign_detail_view, name="campaign_detail"),
]
