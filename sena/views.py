from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Perfil, MetaAhorro

def obtener_rol_usuario(user):
    if not user.is_authenticated:
        return None
    try:
        return user.perfil.rol
    except Exception:
        if user.is_superuser or user.is_staff:
            return 'administrador'
        return 'aprendiz'

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
    rol_usuario = obtener_rol_usuario(request.user)
    return render(request, 'dashboard.html', {'active_tab': 'novedades', 'rol_usuario': rol_usuario})


def usuarios_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    rol_usuario = obtener_rol_usuario(request.user)
    query = request.GET.get('q', '')
    rol_filter = request.GET.get('rol', '')
    
    perfiles = Perfil.objects.select_related('user').all().order_by('user__first_name')
    
    if rol_usuario == 'aprendiz':
        perfiles = perfiles.filter(rol='aprendiz')
        
    if query:
        perfiles = perfiles.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(numero_documento__icontains=query)
        )
        
    if rol_filter and rol_usuario == 'administrador':
        perfiles = perfiles.filter(rol=rol_filter)
        
    context = {
        'perfiles': perfiles,
        'query': query,
        'rol_filter': rol_filter,
        'active_tab': 'usuarios',
        'rol_usuario': rol_usuario
    }
    return render(request, 'usuarios.html', context)


def metas_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    rol_usuario = obtener_rol_usuario(request.user)
    metas = MetaAhorro.objects.filter(user=request.user).order_by('-fecha_creacion')
    
    total_objetivo = sum(meta.monto_objetivo for meta in metas)
    total_ahorrado = sum(meta.monto_actual for meta in metas)
    
    if total_objetivo > 0:
        progreso_general = min(int((total_ahorrado / total_objetivo) * 100), 100)
    else:
        progreso_general = 0
        
    context = {
        'metas': metas,
        'total_objetivo': total_objetivo,
        'total_ahorrado': total_ahorrado,
        'progreso_general': progreso_general,
        'active_tab': 'metas',
        'rol_usuario': rol_usuario
    }
    return render(request, 'metas.html', context)


def crear_meta(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        monto_objetivo = request.POST.get('monto_objetivo')
        monto_actual = request.POST.get('monto_actual') or 0.00
        fecha_limite = request.POST.get('fecha_limite')
        
        try:
            MetaAhorro.objects.create(
                user=request.user,
                nombre=nombre,
                monto_objetivo=monto_objetivo,
                monto_actual=monto_actual,
                fecha_limite=fecha_limite
            )
            messages.success(request, f'Meta "{nombre}" creada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear la meta: {e}')
            
    return redirect('metas')


def actualizar_progreso_meta(request, meta_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        try:
            meta = MetaAhorro.objects.get(id=meta_id, user=request.user)
            cantidad_abono = float(request.POST.get('cantidad_abono', 0))
            meta.monto_actual = float(meta.monto_actual) + cantidad_abono
            meta.save()
            messages.success(request, f'Se abonaron ${cantidad_abono:,.2f} a la meta "{meta.nombre}".')
        except MetaAhorro.DoesNotExist:
            messages.error(request, 'Meta no encontrada.')
        except Exception as e:
            messages.error(request, f'Error al registrar el abono: {e}')
            
    return redirect('metas')


def editar_meta(request, meta_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        try:
            meta = MetaAhorro.objects.get(id=meta_id, user=request.user)
            meta.nombre = request.POST.get('nombre')
            meta.monto_objetivo = request.POST.get('monto_objetivo')
            meta.fecha_limite = request.POST.get('fecha_limite')
            meta.save()
            messages.success(request, f'Meta "{meta.nombre}" actualizada exitosamente.')
        except MetaAhorro.DoesNotExist:
            messages.error(request, 'Meta no encontrada.')
        except Exception as e:
            messages.error(request, f'Error al actualizar la meta: {e}')
            
    return redirect('metas')


def eliminar_meta(request, meta_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        try:
            meta = MetaAhorro.objects.get(id=meta_id, user=request.user)
            nombre = meta.nombre
            meta.delete()
            messages.success(request, f'Meta "{nombre}" eliminada correctamente.')
        except MetaAhorro.DoesNotExist:
            messages.error(request, 'Meta no encontrada.')
        except Exception as e:
            messages.error(request, f'Error al eliminar la meta: {e}')
            
    return redirect('metas')


def editar_usuario(request, perfil_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    rol_actual = obtener_rol_usuario(request.user)
    if rol_actual != 'administrador':
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            perfil = Perfil.objects.select_related('user').get(id=perfil_id)
            user = perfil.user
            
            primer_nombre = request.POST.get('primer_nombre')
            segundo_nombre = request.POST.get('segundo_nombre', '')
            primer_apellido = request.POST.get('primer_apellido')
            segundo_apellido = request.POST.get('segundo_apellido', '')
            email = request.POST.get('email')
            rol = request.POST.get('rol')
            numero_ficha = request.POST.get('numero_ficha', '')
            
            user.first_name = f"{primer_nombre} {segundo_nombre}".strip()
            user.last_name = f"{primer_apellido} {segundo_apellido}".strip()
            user.email = email
            user.save()
            
            perfil.rol = rol
            perfil.numero_ficha = numero_ficha if numero_ficha and rol == 'aprendiz' else None
            perfil.save()
            
            messages.success(request, f'Usuario "{user.get_full_name()}" actualizado correctamente.')
        except Perfil.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al actualizar el usuario: {e}')
            
    return redirect('usuarios')


def eliminar_usuario(request, perfil_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    rol_actual = obtener_rol_usuario(request.user)
    if rol_actual != 'administrador':
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            perfil = Perfil.objects.select_related('user').get(id=perfil_id)
            user = perfil.user
            nombre = user.get_full_name() or user.username
            
            if user == request.user:
                messages.error(request, 'No puedes eliminar tu propio usuario.')
            else:
                user.delete()
                messages.success(request, f'Usuario "{nombre}" eliminado correctamente.')
        except Perfil.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el usuario: {e}')
            
    return redirect('usuarios')


def logout_view(request):
    logout(request)
    return redirect('login')
