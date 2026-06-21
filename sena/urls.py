from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/usuarios/', views.usuarios_view, name='usuarios'),
    path('dashboard/metas/', views.metas_view, name='metas'),
    path('dashboard/metas/crear/', views.crear_meta, name='crear_meta'),
    path('dashboard/metas/actualizar/<int:meta_id>/', views.actualizar_progreso_meta, name='actualizar_progreso_meta'),
    path('dashboard/metas/editar/<int:meta_id>/', views.editar_meta, name='editar_meta'),
    path('dashboard/metas/eliminar/<int:meta_id>/', views.eliminar_meta, name='eliminar_meta'),
    path('logout/', views.logout_view, name='logout'),
]
