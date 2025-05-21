# postulaciones/models.py
from django.db import models
from django.conf import settings
from perfiles.models import Interesado, Curriculum
from vacantes.models import Vacante


class BusquedaGuardada(models.Model):
    interesado = models.ForeignKey(Interesado, on_delete=models.CASCADE, related_name='busquedas_guardadas')
    palabras_clave = models.TextField(blank=True)
    categoria = models.ForeignKey('perfiles.Categoria', on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    salario_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_empleo = models.CharField(max_length=20, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    notificacion_activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Búsqueda Guardada'
        verbose_name_plural = 'Búsquedas Guardadas'

    def __str__(self):
        return f"Búsqueda de {self.interesado} - {self.palabras_clave}"


class VacanteGuardada(models.Model):
    interesado = models.ForeignKey(Interesado, on_delete=models.CASCADE, related_name='vacantes_guardadas')
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='guardada_por')
    fecha_guardado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacante Guardada'
        verbose_name_plural = 'Vacantes Guardadas'

    def __str__(self):
        return f"{self.interesado} guardó {self.vacante.titulo}"


class Postulacion(models.Model):
    ESTADO_CHOICES = (
        ('recibida', 'Recibida'),
        ('en_revision', 'En Revisión'),
        ('entrevista', 'Entrevista'),
        ('rechazada', 'Rechazada'),
        ('contratado', 'Contratado'),
    )

    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='postulaciones')
    interesado = models.ForeignKey(Interesado, on_delete=models.CASCADE, related_name='postulaciones')
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='postulaciones')
    carta_presentacion = models.TextField(blank=True)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='recibida')
    fecha_actualizacion_estado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Postulación'
        verbose_name_plural = 'Postulaciones'

    def __str__(self):
        return f"{self.interesado} a {self.vacante.titulo}"


class Mensaje(models.Model):
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name='mensajes')
    emisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"Mensaje de {self.emisor} a {self.receptor}"


class Notificacion(models.Model):
    TIPO_CHOICES = (
        ('postulacion', 'Postulación'),
        ('mensaje', 'Mensaje'),
        ('estado', 'Cambio de Estado'),
        ('sistema', 'Sistema'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    contenido = models.TextField()
    enlace = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"Notificación para {self.usuario}: {self.tipo}"


class ConfiguracionNotificaciones(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='config_notificaciones')
    tipo_notificacion = models.CharField(max_length=50)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Configuración de Notificaciones'
        verbose_name_plural = 'Configuraciones de Notificaciones'

    def __str__(self):
        return f"Config de {self.usuario}: {self.tipo_notificacion}"