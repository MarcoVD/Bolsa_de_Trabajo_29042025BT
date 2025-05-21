# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from perfiles.models import Interesado, Reclutador
from vacantes.models import Vacante


def home(request):
    """Página de inicio pública"""
    vacantes_destacadas = Vacante.objects.filter(
        estado_vacante='publicada',
        aprobada=True,
        destacada=True
    ).order_by('-fecha_publicacion')[:5]

    return render(request, 'core/home.html', {
        'vacantes_destacadas': vacantes_destacadas
    })


@login_required
def dashboard(request):
    """Dashboard personalizado según el rol del usuario"""
    user = request.user

    if user.es_interesado():
        # Dashboard para interesados
        try:
            interesado = user.interesado
            postulaciones_recientes = interesado.postulaciones.order_by('-fecha_postulacion')[:5]
            vacantes_guardadas = interesado.vacantes_guardadas.order_by('-fecha_guardado')[:5]

            return render(request, 'core/dashboard_interesado.html', {
                'interesado': interesado,
                'postulaciones_recientes': postulaciones_recientes,
                'vacantes_guardadas': vacantes_guardadas
            })
        except Interesado.DoesNotExist:
            messages.error(request, "Perfil de interesado no encontrado.")
            return redirect('crear_perfil_interesado')

    elif user.es_reclutador():
        # Dashboard para reclutadores
        try:
            reclutador = user.reclutador

            if not reclutador.aprobado:
                return render(request, 'core/reclutador_pendiente.html')

            vacantes_activas = reclutador.vacantes.filter(estado_vacante='publicada')
            postulaciones_pendientes = sum(v.postulaciones.filter(estado='recibida').count() for v in vacantes_activas)

            return render(request, 'core/dashboard_reclutador.html', {
                'reclutador': reclutador,
                'vacantes_activas': vacantes_activas,
                'postulaciones_pendientes': postulaciones_pendientes
            })
        except Reclutador.DoesNotExist:
            messages.error(request, "Perfil de reclutador no encontrado.")
            return redirect('crear_perfil_reclutador')

    elif user.es_administrador():
        # Dashboard para administradores
        reclutadores_pendientes = Reclutador.objects.filter(aprobado=False).count()
        vacantes_pendientes = Vacante.objects.filter(aprobada=False, estado_vacante='borrador').count()

        return render(request, 'core/dashboard_admin.html', {
            'reclutadores_pendientes': reclutadores_pendientes,
            'vacantes_pendientes': vacantes_pendientes
        })

    # Caso de error o rol no reconocido
    messages.error(request, "No se pudo determinar el tipo de usuario.")
    return redirect('home')