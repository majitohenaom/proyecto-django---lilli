from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'get_nombre_completo', 'rol', 'numero_ficha', 'fecha_registro']
    list_filter = ['rol', 'tipo_documento']
    search_fields = ['numero_documento', 'user__first_name', 'user__last_name']
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name()
    get_nombre_completo.short_description = 'Nombre Completo'
