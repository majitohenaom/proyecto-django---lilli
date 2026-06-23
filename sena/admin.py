from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Perfil, MetaAhorro, Abono

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'get_nombre_completo', 'tipo_documento', 'rol', 'numero_ficha', 'fecha_registro']
    list_filter = ['rol', 'tipo_documento']
    search_fields = ['numero_documento', 'user__first_name', 'user__last_name']
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name()
    get_nombre_completo.short_description = 'Nombre Completo'


@admin.register(MetaAhorro)
class MetaAhorroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'user', 'monto_objetivo', 'monto_actual', 'fecha_limite', 'estado']
    list_filter = ['fecha_limite']
    search_fields = ['nombre', 'user__username', 'user__first_name']
    readonly_fields = ['fecha_creacion']

    def estado(self, obj):
        return obj.estado
    estado.short_description = 'Estado'


@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ['meta', 'cantidad', 'fecha', 'notas']
    list_filter = ['fecha', 'meta__user']
    search_fields = ['meta__nombre', 'notas']
    readonly_fields = ['fecha']
