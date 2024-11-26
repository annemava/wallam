from django.urls import path
from core.views import HomePageView, WorkPageView, ContactPageView, AnnoncePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('comment-ca-marche', WorkPageView.as_view(), name='works'),
    path('contact', ContactPageView.as_view(), name='contact'),
    path('annonce', AnnoncePageView.as_view(), name='annonce'),
]
