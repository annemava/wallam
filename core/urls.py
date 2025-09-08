from django.urls import path
from core.views import *

urlpatterns = [
    path('', homepage, name='index'),
    path('annonce', AnnoncePageView.as_view(), name='annonce'),
    path('cagnotte', CagnottePageView.as_view(), name='cagnotte'),
    path("cgu", CguPageView.as_view(), name="cgu"),
    path("comment-ca-marche", HowWorkPageView.as_view(), name="how_it_work"),
    path("faq", FaqPageView.as_view(), name="faq"),
    path("garantie-securite", GarantieSecuritePageView.as_view(), name="garantie_securite"),
    path("mention-legale", MentionLegalePageView.as_view(), name="mention_legale"),
    path("tarifs", TarifsPageView.as_view(), name="tarifs"),
    path("qui-sommes-nous", SommesNousPageView.as_view(), name="qui_sommes_nous"),
    path("campaing-donation-list", campaing_donation_list, name="campaing_donation_list"),
    path("reclamation", ReclamationPageView.as_view(), name="reclamation"),
    path('reclamation/', reclamation_view, name='reclamation'),
    path('contact/', contact_view, name='contact'),
    path('404', ErrorPageView.as_view(), name='404'),
    path("conversations/", conversations_list, name="conversations_list"),
    path("conversation/<int:conversation_id>/", conversation_detail, name="conversation_detail"),
    path("conversation/start/<int:pk>/", start_conversation, name="start_conversation"),
]