from django.contrib import admin

# Register your models here.

from .models import Empresas, Correos, Plantillas, Intentos, Status_Mail, Status_Web

admin.site.register(Intentos)
admin.site.register(Empresas)
admin.site.register(Correos)
admin.site.register(Plantillas)
admin.site.register(Status_Mail)
admin.site.register(Status_Web)
