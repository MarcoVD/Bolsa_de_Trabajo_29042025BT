# perfiles/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Habilidad(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='habilidades')

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return self.nombre


class Interesado(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interesado')
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField(blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Interesado'
        verbose_name_plural = 'Interesados'

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Secretaria(models.Model):
    nombre = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13)
    descripcion = models.TextField(blank=True)
    logo = models.ImageField(upload_to='secretarias/', null=True, blank=True)
    sitio_web = models.URLField(blank=True)
    ciudad = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    direccion = models.TextField()
    TAMAÑO_CHOICES = (
        ('pequeña', 'Pequeña'),
        ('mediana', 'Mediana'),
        ('grande', 'Grande'),
    )
    tamaño = models.CharField(max_length=10, choices=TAMAÑO_CHOICES)
    sector = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Secretaría'
        verbose_name_plural = 'Secretarías'

    def __str__(self):
        return self.nombre


class Reclutador(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reclutador')
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, related_name='reclutadores')
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)
    aprobado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Reclutador'
        verbose_name_plural = 'Reclutadores'

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.secretaria.nombre}"


class Curriculum(models.Model):
    interesado = models.ForeignKey(Interesado, on_delete=models.CASCADE, related_name='curriculums')
    resumen_profesional = models.TextField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Currículum'
        verbose_name_plural = 'Currículums'

    def __str__(self):
        return f"CV de {self.interesado}"


class ExperienciaLaboral(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='experiencias')
    empresa = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    actual = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Experiencia Laboral'
        verbose_name_plural = 'Experiencias Laborales'

    def __str__(self):
        return f"{self.puesto} en {self.empresa}"


class Educacion(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='educacion')
    titulo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Educación'
        verbose_name_plural = 'Educación'

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"


class HabilidadInteresado(models.Model):
    NIVEL_CHOICES = (
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    )

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='habilidades')
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES)

    class Meta:
        verbose_name = 'Habilidad del Interesado'
        verbose_name_plural = 'Habilidades del Interesado'

    def __str__(self):
        return f"{self.habilidad.nombre} - {self.nivel}"


class IdiomaInteresado(models.Model):
    NIVEL_CHOICES = (
        ('A1', 'A1 - Principiante'),
        ('A2', 'A2 - Elemental'),
        ('B1', 'B1 - Intermedio'),
        ('B2', 'B2 - Intermedio Alto'),
        ('C1', 'C1 - Avanzado'),
        ('C2', 'C2 - Maestría'),
        ('nativo', 'Nativo'),
    )

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='idiomas')
    idioma = models.CharField(max_length=50)
    nivel_lectura = models.CharField(max_length=10, choices=NIVEL_CHOICES)
    nivel_escritura = models.CharField(max_length=10, choices=NIVEL_CHOICES)
    nivel_conversacion = models.CharField(max_length=10, choices=NIVEL_CHOICES)

    class Meta:
        verbose_name = 'Idioma del Interesado'
        verbose_name_plural = 'Idiomas del Interesado'

    def __str__(self):
        return f"{self.idioma} - Lectura: {self.nivel_lectura}, Escritura: {self.nivel_escritura}, Conversación: {self.nivel_conversacion}"