from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        numero = request.POST.get('numero_documento')
        password = request.POST.get('password')

        user = authenticate(request, username=numero, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Documento o contraseña incorrectos.')

    return render(request, 'login.html')


def registro_view(request):
    if request.method == 'POST':
        primer_nombre = request.POST.get('primer_nombre')
        segundo_nombre = request.POST.get('segundo_nombre', '')
        primer_apellido = request.POST.get('primer_apellido')
        segundo_apellido = request.POST.get('segundo_apellido', '')
        tipo_documento = request.POST.get('tipo_documento')
        numero = request.POST.get('numero_documento')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        rol = request.POST.get('rol')
        numero_ficha = request.POST.get('numero_ficha', '')

        if password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro')

        if User.objects.filter(username=numero).exists():
            messages.error(request, "Este documento ya está registrado.")
            return redirect('registro')

        first_name = f"{primer_nombre} {segundo_nombre}".strip()
        last_name = f"{primer_apellido} {segundo_apellido}".strip()

        user = User.objects.create_user(
            username=numero,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        from .models import Perfil
        Perfil.objects.create(
            user=user,
            tipo_documento=tipo_documento,
            numero_documento=numero,
            rol=rol,
            numero_ficha=numero_ficha if numero_ficha else None
        )

        messages.success(request, "Registro exitoso. Ahora inicia sesión.")
        return redirect('login')

    return render(request, 'registro.html')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')
