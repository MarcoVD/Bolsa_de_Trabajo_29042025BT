# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import RegistroInteresadoForm, RegistroReclutadorForm, LoginForm


def registro_interesado(request):
    """Vista para registro de interesados/candidatos"""
    if request.method == 'POST':
        form = RegistroInteresadoForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso. Ahora completa tu perfil.")
            return redirect('crear_perfil_interesado')
    else:
        form = RegistroInteresadoForm()

    return render(request, 'usuarios/registro_interesado.html', {'form': form})


def registro_reclutador(request):
    """Vista para registro de reclutadores"""
    if request.method == 'POST':
        form = RegistroReclutadorForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso. Ahora completa el perfil de tu secretaría.")
            return redirect('crear_perfil_reclutador')
    else:
        form = RegistroReclutadorForm()

    return render(request, 'usuarios/registro_reclutador.html', {'form': form})


def login_view(request):
    """Vista para inicio de sesión"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                user.ultimo_acceso = timezone.now()
                user.save()

                return redirect('dashboard')
            else:
                messages.error(request, "Credenciales inválidas")
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})