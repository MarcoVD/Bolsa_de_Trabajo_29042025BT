# vacantes/models.py
from django.db import models
from perfiles.models import Secretaria, Reclutador, Categoria, Habilidad


class Vacante(models.Model):
    TIPO_EMPLEO_CHOICES = (
        ('tiempo_completo', 'Tiempo Completo'),
        ('medio_tiempo', 'Medio Tiempo'),
        ('proyecto', 'Proyecto'),
        ('pasantia', 'Pasantía'),
    )

    MODALIDAD_CHOICES = (
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    )

    ESTADO_VACANTE_CHOICES = (
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
        ('cerrada', 'Cerrada'),
        ('eliminada', 'Eliminada'),
    )

    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, related_name='vacantes')
    reclutador = models.ForeignKey(Reclutador, on_delete=models.CASCADE, related_name='vacantes')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='vacantes')
    estado = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    salario_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_empleo = models.CharField(max_length=20, choices=TIPO_EMPLEO_CHOICES)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_limite = models.DateField()
    estado_vacante = models.CharField(max_length=20, choices=ESTADO_VACANTE_CHOICES, default='borrador')
    aprobada = models.BooleanField(default=False)
    destacada = models.BooleanField(default=False)
    max_postulantes = models.PositiveIntegerField(default=100)
    max_postulaciones_por_interesado = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Vacante'
        verbose_name_plural = 'Vacantes'

    def __str__(self):
        return f"{self.titulo} - {self.secretaria.nombre}"


class RequisitosVacante(models.Model):
    vacante = models.OneToOneField(Vacante, on_delete=models.CASCADE, related_name='requisitos')
    educacion_minima = models.CharField(max_length=100)
    experiencia_minima = models.PositiveIntegerField()  # En años
    descripcion = models.TextField()

    class Meta:
        verbose_name = 'Requisitos de Vacante'
        verbose_name_plural = 'Requisitos de Vacantes'

    def __str__(self):
        return f"Requisitos para {self.vacante.titulo}"


class HabilidadRequerida(models.Model):
    NIVEL_CHOICES = (
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    )

    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='habilidades_requeridas')
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)
    nivel_requerido = models.CharField(max_length=15, choices=NIVEL_CHOICES)
    obligatorio = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Habilidad Requerida'
        verbose_name_plural = 'Habilidades Requeridas'

    def __str__(self):
        return f"{self.habilidad.nombre} - {self.nivel_requerido} - {'Obligatorio' if self.obligatorio else 'Deseable'}"