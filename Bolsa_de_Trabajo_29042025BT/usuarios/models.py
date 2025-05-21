# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('interesado', 'Interesado'),
        ('reclutador', 'Reclutador'),
        ('administrador', 'Administrador'),
    )

    rol = models.CharField(max_length=15, choices=ROL_CHOICES)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username

    def es_interesado(self):
        return self.rol == 'interesado'

    def es_reclutador(self):
        return self.rol == 'reclutador'

    def es_administrador(self):
        return self.rol == 'administrador'