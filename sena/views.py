from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Perfil, MetaAhorro
from django.utils import timezone
import re
import datetime

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
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        numero = request.POST.get('numero_documento', '')
        password = request.POST.get('password', '')

        # Limit special characters
        if not re.match(r'^[a-zA-Z0-9]+$', numero):
            messages.error(request, 'El documento contiene caracteres no permitidos.')
            return render(request, 'login.html')
            
        if not re.match(r'^[a-zA-Z0-9!@#\$%\^&\*\-_]+$', password):
            messages.error(request, 'La contraseña contiene caracteres no permitidos.')
            return render(request, 'login.html')

        user = authenticate(request, username=numero, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Documento o contraseña incorrectos.')

    return render(request, 'login.html')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        primer_nombre = request.POST.get('primer_nombre')
        segundo_nombre = request.POST.get('segundo_nombre', '')
        primer_apellido = request.POST.get('primer_apellido')
        segundo_apellido = request.POST.get('segundo_apellido', '')
        tipo_documento = request.POST.get('tipo_documento', '')
        numero = request.POST.get('numero_documento', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2')
        rol = request.POST.get('rol')
        numero_ficha = request.POST.get('numero_ficha', '')

        # Limit special characters
        if not re.match(r'^[a-zA-Z0-9]+$', numero):
            messages.error(request, 'El documento contiene caracteres no permitidos.')
            return redirect('registro')
            
        if not re.match(r'^[a-zA-Z0-9!@#\$%\^&\*\-_]+$', password):
            messages.error(request, 'La contraseña contiene caracteres no permitidos.')
            return redirect('registro')

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

        if rol == 'administrador':
            user.is_staff = True
            user.save()

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


@login_required
def dashboard(request):
    rol_usuario = obtener_rol_usuario(request.user)
    return render(request, 'dashboard.html', {'active_tab': 'novedades', 'rol_usuario': rol_usuario})


@login_required
def usuarios_view(request):
    rol_usuario = obtener_rol_usuario(request.user)
    query = request.GET.get('q', '')
    rol_filter = request.GET.get('rol', '')
    page_number = request.GET.get('page', 1)

    perfiles_qs = Perfil.objects.select_related('user').all().order_by('user__first_name')

    if rol_usuario == 'aprendiz':
        perfiles_qs = perfiles_qs.filter(rol='aprendiz')

    if query:
        perfiles_qs = perfiles_qs.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(numero_documento__icontains=query)
        )

    if rol_filter and rol_usuario == 'administrador':
        perfiles_qs = perfiles_qs.filter(rol=rol_filter)

    total_usuarios = perfiles_qs.count()

    paginator = Paginator(perfiles_qs, 10)  # 10 usuarios por página
    try:
        perfiles = paginator.page(page_number)
    except PageNotAnInteger:
        perfiles = paginator.page(1)
    except EmptyPage:
        perfiles = paginator.page(paginator.num_pages)

    context = {
        'perfiles': perfiles,
        'total_usuarios': total_usuarios,
        'query': query,
        'rol_filter': rol_filter,
        'active_tab': 'usuarios',
        'rol_usuario': rol_usuario,
        'paginator': paginator,
    }
    return render(request, 'usuarios.html', context)


@login_required
def metas_view(request):
    rol_usuario = obtener_rol_usuario(request.user)
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    todas_metas = MetaAhorro.objects.filter(user=request.user).order_by('-fecha_creacion')

    if query:
        todas_metas = todas_metas.filter(nombre__icontains=query)

    # Calcular totales con una sola consulta a la BD (más eficiente)
    totales = todas_metas.aggregate(
        total_objetivo=Sum('monto_objetivo'),
        total_ahorrado=Sum('monto_actual')
    )
    total_objetivo = totales['total_objetivo'] or 0
    total_ahorrado = totales['total_ahorrado'] or 0

    if total_objetivo > 0:
        progreso_general = min(int((total_ahorrado / total_objetivo) * 100), 100)
    else:
        progreso_general = 0

    paginator = Paginator(todas_metas, 6)  # 6 metas por página (grid 3x2)
    try:
        metas = paginator.page(page_number)
    except PageNotAnInteger:
        metas = paginator.page(1)
    except EmptyPage:
        metas = paginator.page(paginator.num_pages)

    context = {
        'metas': metas,
        'total_objetivo': total_objetivo,
        'total_ahorrado': total_ahorrado,
        'progreso_general': progreso_general,
        'active_tab': 'metas',
        'rol_usuario': rol_usuario,
        'paginator': paginator,
        'query': query,
    }
    return render(request, 'metas.html', context)


@login_required
def crear_meta(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        monto_objetivo = request.POST.get('monto_objetivo')
        monto_actual = request.POST.get('monto_actual') or 0.00
        fecha_limite_str = request.POST.get('fecha_limite')
        
        try:
            # Server-side validation to prevent past dates
            fecha_limite_val = datetime.datetime.strptime(fecha_limite_str, '%Y-%m-%d').date()
            if fecha_limite_val < timezone.now().date():
                messages.error(request, 'La fecha límite no puede estar en el pasado.')
                return redirect('metas')
                
            MetaAhorro.objects.create(
                user=request.user,
                nombre=nombre,
                monto_objetivo=monto_objetivo,
                monto_actual=monto_actual,
                fecha_limite=fecha_limite_val
            )
            messages.success(request, f'Meta "{nombre}" creada exitosamente.')
        except ValueError:
            messages.error(request, 'Formato de fecha límite inválido.')
        except Exception as e:
            messages.error(request, f'Error al crear la meta: {e}')
            
    return redirect('metas')


@login_required
def actualizar_progreso_meta(request, meta_id):
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


@login_required
def editar_meta(request, meta_id):
    if request.method == 'POST':
        try:
            meta = MetaAhorro.objects.get(id=meta_id, user=request.user)
            fecha_limite_str = request.POST.get('fecha_limite')
            
            # Server-side validation to prevent past dates
            try:
                fecha_limite_val = datetime.datetime.strptime(fecha_limite_str, '%Y-%m-%d').date()
                if fecha_limite_val < timezone.now().date():
                    messages.error(request, 'La fecha límite no puede estar en el pasado.')
                    return redirect('metas')
            except ValueError:
                messages.error(request, 'Formato de fecha límite inválido.')
                return redirect('metas')

            meta.nombre = request.POST.get('nombre')
            meta.monto_objetivo = request.POST.get('monto_objetivo')
            meta.fecha_limite = fecha_limite_val
            meta.save()
            messages.success(request, f'Meta "{meta.nombre}" actualizada exitosamente.')
        except MetaAhorro.DoesNotExist:
            messages.error(request, 'Meta no encontrada.')
        except Exception as e:
            messages.error(request, f'Error al actualizar la meta: {e}')
            
    return redirect('metas')


@login_required
def eliminar_meta(request, meta_id):
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


@login_required
def editar_usuario(request, perfil_id):
    rol_actual = obtener_rol_usuario(request.user)
    if rol_actual != 'administrador':
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            perfil = Perfil.objects.select_related('user').get(id=perfil_id)
            user = perfil.user
            
            tipo_documento = request.POST.get('tipo_documento')
            numero_documento = request.POST.get('numero_documento')
            primer_nombre = request.POST.get('primer_nombre')
            primer_apellido = request.POST.get('primer_apellido')
            email = request.POST.get('email')
            rol = request.POST.get('rol')
            numero_ficha = request.POST.get('numero_ficha', '')
            
            # Validation for duplicate document number
            if numero_documento != perfil.numero_documento:
                if User.objects.filter(username=numero_documento).exclude(id=user.id).exists() or Perfil.objects.filter(numero_documento=numero_documento).exclude(id=perfil.id).exists():
                    messages.error(request, 'El número de documento ya está registrado por otro usuario.')
                    return redirect('usuarios')
            
            user.username = numero_documento
            user.first_name = primer_nombre.strip()
            user.last_name = primer_apellido.strip()
            user.email = email
            
            if rol == 'administrador':
                user.is_staff = True
            else:
                user.is_staff = False
                user.is_superuser = False
                
            user.save()
            
            perfil.tipo_documento = tipo_documento
            perfil.numero_documento = numero_documento
            perfil.rol = rol
            perfil.numero_ficha = numero_ficha if numero_ficha and rol == 'aprendiz' else None
            perfil.save()
            
            messages.success(request, f'Usuario "{user.get_full_name()}" actualizado correctamente.')
        except Perfil.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al actualizar el usuario: {e}')
            
    return redirect('usuarios')


@login_required
def eliminar_usuario(request, perfil_id):
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


@login_required
def configuraciones_view(request):
    rol_usuario = obtener_rol_usuario(request.user)
    perfil = getattr(request.user, 'perfil', None)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            tipo_documento = request.POST.get('tipo_documento')
            numero_documento = request.POST.get('numero_documento', '')
            primer_nombre = request.POST.get('primer_nombre')
            primer_apellido = request.POST.get('primer_apellido')
            email = request.POST.get('email')
            numero_ficha = request.POST.get('numero_ficha', '')

            # Capa 2: Validación Regex servidor - campo crítico
            if not re.match(r'^[a-zA-Z0-9]+$', numero_documento):
                messages.error(request, 'El número de documento contiene caracteres no permitidos.')
                return redirect('configuraciones')
            
            # Validation for duplicate document number
            if perfil and numero_documento != perfil.numero_documento:
                if User.objects.filter(username=numero_documento).exclude(id=request.user.id).exists() or Perfil.objects.filter(numero_documento=numero_documento).exclude(user_id=request.user.id).exists():
                    messages.error(request, 'El número de documento ya está registrado por otro usuario.')
                    return redirect('configuraciones')
            
            request.user.username = numero_documento
            request.user.first_name = primer_nombre.strip()
            request.user.last_name = primer_apellido.strip()
            request.user.email = email
            request.user.save()
            
            if perfil:
                perfil.tipo_documento = tipo_documento
                perfil.numero_documento = numero_documento
                perfil.numero_ficha = numero_ficha if numero_ficha and perfil.rol == 'aprendiz' else None
                perfil.save()
                
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('configuraciones')
            
        elif action == 'change_password':
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')

            # Capa 2: Validación Regex servidor - campo crítico contraseña
            if not re.match(r'^[a-zA-Z0-9!@#\$%\^&\*\-_]+$', new_password):
                messages.error(request, 'La nueva contraseña contiene caracteres no permitidos.')
                return redirect('configuraciones')
            
            if not request.user.check_password(current_password):
                messages.error(request, 'La contraseña actual es incorrecta.')
                return redirect('configuraciones')
                
            if new_password != confirm_password:
                messages.error(request, 'Las nuevas contraseñas no coinciden.')
                return redirect('configuraciones')
                
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep the user logged in
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('configuraciones')
            
    context = {
        'active_tab': 'configuraciones',
        'rol_usuario': rol_usuario,
        'perfil': perfil
    }
    return render(request, 'configuraciones.html', context)


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')
