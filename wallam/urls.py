from django.conf import settings
from django.conf.urls.static import static
"""
URL configuration for wallam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import urls as core_url
from core.views import login_view, register_view, logout_view, password_reset_view, password_reset_confirm_view
from campaign import urls as campaign_url
from donation import urls as announce_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(core_url)),
    path('', include(campaign_url)),
    path('', include(announce_url)),
    path('connexion', login_view, name='login'),
    path('deconnexion', logout_view, name='logout'),
    path('enregistrement', register_view, name='register'),
    path('mot-de-passe-oublie/', password_reset_view, name='password_reset'),
    path('mot-de-passe-reset/<int:uid>/<str:token>/', password_reset_confirm_view, name='password_reset_confirm'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)