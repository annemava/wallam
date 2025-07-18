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
    path('404', ErrorPageView.as_view(), name='404'),
]
