from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Association)
admin.site.register(Particulier)
admin.site.register(Contact)
admin.site.register(Reclamation)