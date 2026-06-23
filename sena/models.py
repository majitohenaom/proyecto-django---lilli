from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
    ]
    
    ROL_CHOICES = [
        ('aprendiz', 'Aprendiz'),
        ('administrador', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    numero_ficha = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.numero_documento}"
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


class MetaAhorro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas_ahorro')
    nombre = models.CharField(max_length=100)
    monto_objetivo = models.DecimalField(max_digits=12, decimal_places=2)
    monto_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha_limite = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def progreso(self):
        if self.monto_objetivo > 0:
            return min(int((self.monto_actual / self.monto_objetivo) * 100), 100)
        return 0

    @property
    def dias_restantes(self):
        delta = self.fecha_limite - timezone.now().date()
        return delta.days

    @property
    def dias_vencidos(self):
        if self.dias_restantes < 0:
            return abs(self.dias_restantes)
        return 0

    @property
    def estado(self):
        if self.monto_actual >= self.monto_objetivo:
            return 'completada'
        elif self.fecha_limite < timezone.now().date():
            return 'vencida'
        else:
            return 'en_progreso'

    def __str__(self):
        return f"{self.nombre} - {self.user.username}"

    class Meta:
        verbose_name = 'Meta de Ahorro'
        verbose_name_plural = 'Metas de Ahorro'