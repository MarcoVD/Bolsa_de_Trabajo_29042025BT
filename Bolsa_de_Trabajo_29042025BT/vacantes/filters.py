# vacantes/filters.py
import django_filters
from .models import Vacante


class VacanteFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    categoria = django_filters.ModelChoiceFilter(queryset=Categoria.objects.all())
    ciudad = django_filters.CharFilter(lookup_expr='icontains')
    estado = django_filters.CharFilter(lookup_expr='icontains')
    salario_min = django_filters.NumberFilter(field_name='salario_min', lookup_expr='gte')
    tipo_empleo = django_filters.ChoiceFilter(choices=Vacante.TIPO_EMPLEO_CHOICES)
    modalidad = django_filters.ChoiceFilter(choices=Vacante.MODALIDAD_CHOICES)

    class Meta:
        model = Vacante
        fields = ['titulo', 'categoria', 'ciudad', 'estado', 'salario_min', 'tipo_empleo', 'modalidad']