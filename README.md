# 💼 SENA GDF — Sistema de Gestión de Finanzas

<div align="center">

**Aplicación web full-stack construida con Django 5 y MySQL**  
Diseñada para que los aprendices del SENA puedan gestionar sus metas de ahorro personales,
registrar abonos y hacer seguimiento financiero de sus objetivos de manera visual e intuitiva.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?style=flat-square&logo=django)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange?style=flat-square&logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)

</div>

---

## 📋 Tabla de Contenido

1. [¿Qué es SENA GDF?](#-qué-es-sena-gdf)
2. [¿Para qué sirve?](#-para-qué-sirve)
3. [Características Principales](#-características-principales)
4. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
5. [Estructura Detallada del Proyecto](#-estructura-detallada-del-proyecto)
6. [Modelos de Base de Datos](#-modelos-de-base-de-datos)
7. [Vistas y Lógica del Servidor](#-vistas-y-lógica-del-servidor)
8. [URLs y Rutas del Sistema](#-urls-y-rutas-del-sistema)
9. [Roles y Permisos](#-roles-y-permisos)
10. [Diseño de la Interfaz](#-diseño-de-la-interfaz)
11. [Seguridad Implementada](#-seguridad-implementada)
12. [Instalación Paso a Paso](#-instalación-paso-a-paso)
13. [Configuración de Variables de Entorno](#-configuración-de-variables-de-entorno)
14. [Base de Datos en phpMyAdmin](#-base-de-datos-en-phpmyadmin)
15. [Cómo Ejecutar el Proyecto](#-cómo-ejecutar-el-proyecto)
16. [Panel de Administración Django](#-panel-de-administración-django)
17. [Dependencias del Proyecto](#-dependencias-del-proyecto)
18. [Flujo Completo de la Aplicación](#-flujo-completo-de-la-aplicación)
19. [Notas para el Desarrollador](#-notas-para-el-desarrollador)

---

## 🌟 ¿Qué es SENA GDF?

**SENA GDF** (Sistema de Gestión de Finanzas) es una aplicación web desarrollada como proyecto formativo dentro del programa del SENA. Es un sistema **interno y privado** que permite a los aprendices e instructores llevar un control organizado y digital de sus metas financieras personales.

El sistema fue construido completamente desde cero usando el framework **Django** (Python), con una base de datos relacional **MySQL**, y una interfaz moderna y responsiva basada en **Bootstrap 5** con estilos personalizados en CSS.

> **Contexto de uso:** El sistema está diseñado para ser ejecutado en un entorno local (intranet o servidor de desarrollo), aprovechando XAMPP como servidor MySQL y Django como servidor web de desarrollo.

---

## 🎯 ¿Para qué sirve?

El sistema resuelve un problema muy común entre los aprendices del SENA: **la falta de herramientas digitales para planificar y hacer seguimiento del ahorro personal**. Con SENA GDF puedes:

- **Definir metas de ahorro específicas:** Por ejemplo, "Comprar una laptop" con un monto objetivo de $2.000.000 COP y una fecha límite de 6 meses.
- **Registrar pagos (abonos) progresivos:** Cada vez que ahorras una cantidad, la registras en el sistema con una nota opcional (Ej: "Quincena de junio").
- **Ver el historial completo de pagos:** Un modal desplegable muestra todos los abonos realizados hacia cada meta, con fecha, monto y nota.
- **Visualizar el progreso:** Cada meta muestra una barra de progreso animada y el porcentaje completado.
- **Conocer el estado de cada meta:** El sistema clasifica automáticamente las metas como `En Progreso`, `Completada` o `Vencida` según la fecha y los montos.
- **Gestionar usuarios (administradores):** Los usuarios con rol `administrador` pueden crear, editar y eliminar cuentas de otros usuarios.

---

## ✨ Características Principales

### 🔐 Módulo de Autenticación

- **Login seguro** con tres campos obligatorios:
  1. Tipo de documento (CC, TI, CE) — menú desplegable
  2. Número de documento — campo de texto
  3. Contraseña — campo enmascarado con botón para mostrar/ocultar
- El sistema **valida que el tipo de documento coincida** con el registrado en el perfil. Si un usuario tiene CC registrada pero intenta entrar con TI, el sistema lo rechaza.
- Al hacer clic en "Ingresar al Panel", el botón se deshabilita y muestra un spinner de carga para evitar múltiples envíos.
- **Registro de nuevos usuarios** con formulario completo: nombre, apellidos, tipo y número de documento, email, contraseña (con confirmación), rol y número de ficha.

### 🎯 Módulo de Metas de Ahorro

- **Crear metas** con nombre descriptivo, monto objetivo en COP, ahorro inicial opcional y fecha límite.
- **Validación de fechas:** El sistema impide (tanto en frontend como en backend) crear metas con fechas en el pasado.
- **Editar metas:** Modificar nombre, monto objetivo y fecha límite en cualquier momento.
- **Eliminar metas** con confirmación de seguridad.
- **Tres estados automáticos:**
  - 🟢 `En Progreso`: La fecha no ha vencido y el monto aún no se ha alcanzado.
  - ✅ `Completada`: El monto actual es igual o mayor al objetivo.
  - 🔴 `Vencida`: La fecha límite pasó sin alcanzar el objetivo.
- Indicador visual de días restantes: verde (más de 7 días), amarillo (7 días o menos) o rojo (vencida hace N días).
- **Barra de progreso animada** que cambia de color según el estado (magenta, verde o rojo).
- **Búsqueda de metas** por nombre con campo de texto en tiempo real.
- **Paginación** de 6 metas por página (grid de 2×3).

### 💰 Módulo de Abonos

- **Registrar abonos** desde un modal en cada tarjeta de meta activa (no vencida, no completada).
- Cada abono guarda: meta relacionada, cantidad, fecha/hora exacta y nota opcional.
- **Validación:** el monto del abono debe ser mayor a $0.
- Al registrar un abono, el sistema suma automáticamente el monto al `monto_actual` de la meta.
- Campo de **Notas opcionales** para describir el origen del dinero (Ej: "Bono de trabajo", "Mesada de diciembre").

### 📋 Módulo de Historial de Abonos

- Botón **"Ver Historial"** en cada tarjeta de meta (visible siempre, independiente del estado).
- Modal con **tabla completa** de todos los abonos realizados hacia esa meta:
  - Número de abono (en orden descendente, el más reciente primero)
  - Fecha y hora del abono
  - Monto abonado formateado en COP
  - Notas del abono (o un guion si no tiene)
- Resumen al final: cantidad total de abonos y **suma total acumulada**.
- Si no hay abonos, muestra un mensaje amigable invitando a registrar el primero.

### 👥 Módulo de Usuarios

- **Listado de usuarios** con información completa: nombre, documento, email, rol y ficha.
- **Búsqueda** por nombre, documento o email.
- **Filtro por rol** (solo administradores).
- **Paginación** de 10 usuarios por página.
- **Editar** cualquier usuario: cambiar datos personales, tipo de documento, rol y ficha.
- **Eliminar** usuarios con protección: un administrador no puede eliminarse a sí mismo.
- Los **aprendices** solo ven la lista de otros aprendices (no administradores).

### ⚙️ Módulo de Configuraciones

- **Editar perfil propio:** tipo de documento, número de documento, nombre, apellido, email y ficha.
- **Cambiar contraseña** con verificación de la contraseña actual y confirmación de la nueva.
- Al cambiar la contraseña, la sesión se mantiene activa (no cierra la sesión del usuario).

---

## 🛠 Tecnologías Utilizadas

### Backend

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **Python** | 3.11+ | Lenguaje base del proyecto |
| **Django** | 5.x | Framework web MVC completo |
| **mysqlclient** | Latest | Conector de Django con MySQL |
| **python-dotenv** | Latest | Carga de variables de entorno desde `.env` |
| **Django Humanize** | Incluido | Formateo de números (intcomma: 1500000 → 1,500,000) |

### Base de Datos

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **MySQL** | 8.x | Motor de base de datos relacional |
| **phpMyAdmin** | 5.2.1 | Interfaz visual para administrar MySQL |
| **XAMPP** | Latest | Servidor local Apache + MySQL |

### Frontend

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **Bootstrap** | 5.3 (local) | Framework CSS responsivo |
| **Bootstrap Icons** | 1.x (local) | Iconografía (más de 2000 íconos) |
| **HTMX** | 1.x (local) | Navegación SPA sin recargas de página |
| **JavaScript** | Vanilla ES6+ | Lógica de modales e interacciones |
| **Google Fonts** | CDN | Tipografía Outfit (300, 400, 500, 600, 700, 800) |
| **CSS personalizado** | — | Variables CSS, animaciones, glassmorphism |

> 📦 **Nota sobre estáticos locales:** Bootstrap, Bootstrap Icons y HTMX se sirven **desde el servidor local** (`/static/`). Esto garantiza que el proyecto funcione **sin conexión a internet**, solo requiriendo conexión para la fuente de Google.

---

## 📁 Estructura Detallada del Proyecto

```
djangoLilliana/                          ← Raíz del proyecto
│
├── manage.py                            ← CLI de Django (correr servidor, migraciones, etc.)
├── .env                                 ← Variables de entorno (SECRET_KEY, DB, etc.) ¡NO subir a Git!
├── .gitignore                           ← Archivos y carpetas excluidos de Git
├── requirements.txt                     ← Lista de dependencias Python del proyecto
├── README.md                            ← Este archivo de documentación
│
├── mi_proyecto/                         ← Paquete de configuración principal de Django
│   ├── __init__.py
│   ├── settings.py                      ← Toda la configuración de Django:
│   │                                        - Base de datos MySQL
│   │                                        - Apps instaladas
│   │                                        - Rutas de estáticos y templates
│   │                                        - Zona horaria y lenguaje
│   ├── urls.py                          ← Router principal: incluye las URLs de la app 'sena'
│   ├── wsgi.py                          ← Punto de entrada para servidores WSGI (producción)
│   └── asgi.py                          ← Punto de entrada para servidores ASGI (async)
│
├── env/                                 ← Entorno virtual de Python (NO subir a Git)
│   └── Lib/site-packages/               ← Todas las librerías instaladas
│
└── sena/                                ← Aplicación Django principal del proyecto
    │
    ├── __init__.py                      ← Marca 'sena' como paquete Python
    ├── apps.py                          ← Configuración de la app: nombre 'sena'
    ├── models.py                        ← Definición de los 3 modelos: Perfil, MetaAhorro, Abono
    ├── views.py                         ← Toda la lógica de negocio y respuestas HTTP
    ├── urls.py                          ← 14 rutas URL de la aplicación
    ├── admin.py                         ← Registro de modelos en el panel /admin/
    ├── tests.py                         ← Archivo de pruebas unitarias (base)
    │
    ├── migrations/                      ← Historial de cambios aplicados a la BD
    │   ├── __init__.py
    │   ├── 0001_initial.py              ← Crea la tabla sena_perfil
    │   ├── 0002_metaahorro.py           ← Crea la tabla sena_metaahorro
    │   ├── 0003_alter_perfil_rol.py     ← Ajusta los roles válidos (aprendiz, administrador)
    │   └── 0004_abono.py               ← Crea la tabla sena_abono (historial de pagos)
    │
    ├── templates/                       ← Plantillas HTML del proyecto
    │   ├── base_dashboard.html          ← Layout maestro: navbar superior + sidebar + área de contenido
    │   │                                   Todos los demás templates del dashboard lo extienden
    │   ├── login.html                   ← Página de inicio de sesión (standalone, no extiende base)
    │   ├── registro.html                ← Formulario de registro de nuevos usuarios
    │   ├── dashboard.html               ← Pantalla principal de novedades (solo administradores)
    │   ├── metas.html                   ← Grid de metas de ahorro con modales (crear, editar, abonar, historial)
    │   ├── usuarios.html                ← Tabla de usuarios con modales de edición
    │   └── configuraciones.html         ← Formulario de perfil propio y cambio de contraseña
    │
    └── static/sena/                     ← Archivos estáticos servidos por Django
        ├── css/
        │   ├── bootstrap.min.css        ← Bootstrap 5.3 compilado y minificado
        │   ├── bootstrap-icons.min.css  ← Hoja de estilos de Bootstrap Icons
        │   ├── sena-theme.css           ← Estilos personalizados del sistema SENA GDF:
        │   │                               variables de color magenta, sombras, animaciones
        │   └── fonts/                   ← Fuentes de Bootstrap Icons (para íconos offline)
        │       ├── bootstrap-icons.woff
        │       └── bootstrap-icons.woff2
        └── js/
            ├── bootstrap.bundle.min.js  ← Bootstrap JS + Popper.js (para modales, dropdowns)
            └── htmx.min.js              ← HTMX para navegación sin recarga completa de página
```

---

## 🗄 Modelos de Base de Datos

El proyecto usa **3 modelos propios** más los modelos nativos de Django (`auth_user`, `auth_group`, etc.).

---

### 📄 Modelo `Perfil`

**Archivo:** `sena/models.py`  
**Tabla en MySQL:** `sena_perfil`  
**Propósito:** Extender el modelo de usuario nativo de Django (`auth_user`) con información específica del sistema, como el tipo y número de documento, el rol dentro del sistema y la ficha del SENA.

```python
class Perfil(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
    ]

    ROL_CHOICES = [
        ('aprendiz', 'Aprendiz'),
        ('administrador', 'Administrador'),
    ]

    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)
    rol            = models.CharField(max_length=20, choices=ROL_CHOICES)
    numero_ficha   = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
```

**Descripción de campos:**

| Campo | Tipo Django | Tipo MySQL | Restricciones | Descripción |
|-------|------------|------------|---------------|-------------|
| `id` | BigAutoField | BIGINT | PK, Auto | ID interno generado automáticamente |
| `user` | OneToOneField | BIGINT (FK) | NOT NULL, UNIQUE | Referencia a `auth_user.id`. Si se borra el usuario, se borra el perfil |
| `tipo_documento` | CharField(2) | VARCHAR(2) | NOT NULL | Solo acepta 'CC', 'TI' o 'CE' |
| `numero_documento` | CharField(20) | VARCHAR(20) | NOT NULL, UNIQUE | Identificador único por persona. También es el `username` en `auth_user` |
| `rol` | CharField(20) | VARCHAR(20) | NOT NULL | Solo acepta 'aprendiz' o 'administrador' |
| `numero_ficha` | CharField(20) | VARCHAR(20) | NULL, BLANK | Solo aplica para aprendices. Número de ficha del programa SENA |
| `fecha_registro` | DateTimeField | DATETIME | auto_now_add | Se guarda automáticamente al crear el perfil, no se puede modificar |

**Relación:** Un `Perfil` pertenece a exactamente un `User`. Un `User` tiene exactamente un `Perfil`. (OneToOne)

---

### 📄 Modelo `MetaAhorro`

**Archivo:** `sena/models.py`  
**Tabla en MySQL:** `sena_metaahorro`  
**Propósito:** Representa un objetivo financiero personal de un usuario. Almacena el monto que se quiere alcanzar, cuánto se ha ahorrado hasta ahora y la fecha límite para lograrlo.

```python
class MetaAhorro(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas_ahorro')
    nombre         = models.CharField(max_length=100)
    monto_objetivo = models.DecimalField(max_digits=12, decimal_places=2)
    monto_actual   = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha_limite   = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

**Descripción de campos:**

| Campo | Tipo Django | Tipo MySQL | Restricciones | Descripción |
|-------|------------|------------|---------------|-------------|
| `id` | BigAutoField | BIGINT | PK, Auto | ID de la meta |
| `user` | ForeignKey | BIGINT (FK) | NOT NULL | Referencia a `auth_user.id`. Si se borra el usuario, se borran sus metas |
| `nombre` | CharField(100) | VARCHAR(100) | NOT NULL | Nombre descriptivo de la meta (Ej: "Laptop", "Vacaciones") |
| `monto_objetivo` | DecimalField | DECIMAL(12,2) | NOT NULL | Monto total a alcanzar en COP. Máx: 9,999,999,999.99 |
| `monto_actual` | DecimalField | DECIMAL(12,2) | default=0.00 | Suma de todos los abonos registrados hasta la fecha |
| `fecha_limite` | DateField | DATE | NOT NULL | Fecha máxima para cumplir la meta. No puede ser en el pasado al crear |
| `fecha_creacion` | DateTimeField | DATETIME | auto_now_add | Se guarda al crear la meta, solo lectura |

**Propiedades calculadas (no se guardan en BD, se calculan al vuelo):**

```python
def progreso(self):
    # Retorna el porcentaje completado (0-100)
    # Ej: monto_actual=750.000, monto_objetivo=1.500.000 → 50%
    if self.monto_objetivo > 0:
        return min(int((self.monto_actual / self.monto_objetivo) * 100), 100)
    return 0

@property
def dias_restantes(self):
    # Días que faltan para la fecha límite (negativo si ya venció)
    delta = self.fecha_limite - timezone.now().date()
    return delta.days

@property
def dias_vencidos(self):
    # Cuántos días han pasado desde que venció (solo si venció)
    if self.dias_restantes < 0:
        return abs(self.dias_restantes)
    return 0

@property
def estado(self):
    # Estado automático basado en fechas y montos
    if self.monto_actual >= self.monto_objetivo:
        return 'completada'    # ✅ Objetivo alcanzado
    elif self.fecha_limite < timezone.now().date():
        return 'vencida'       # 🔴 Fecha pasó sin completarse
    else:
        return 'en_progreso'   # 🟡 Todavía en curso
```

**Relación:** Un `User` puede tener muchas `MetaAhorro`. Una `MetaAhorro` pertenece a un solo `User`. (ForeignKey Many-to-One)

---

### 📄 Modelo `Abono`

**Archivo:** `sena/models.py`  
**Tabla en MySQL:** `sena_abono`  
**Propósito:** Registra cada pago individual que el usuario hace hacia una meta de ahorro. Permite mantener un historial detallado y trazable de todos los movimientos de dinero. Al registrar un abono, el sistema automáticamente suma el monto al `monto_actual` de la meta relacionada.

```python
class Abono(models.Model):
    meta     = models.ForeignKey(MetaAhorro, on_delete=models.CASCADE, related_name='abonos')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    fecha    = models.DateTimeField(auto_now_add=True)
    notas    = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-fecha']  # Los abonos más recientes aparecen primero
```

**Descripción de campos:**

| Campo | Tipo Django | Tipo MySQL | Restricciones | Descripción |
|-------|------------|------------|---------------|-------------|
| `id` | BigAutoField | BIGINT | PK, Auto | ID del abono |
| `meta` | ForeignKey | BIGINT (FK) | NOT NULL | Meta a la que pertenece. Si se borra la meta, se borran sus abonos |
| `cantidad` | DecimalField | DECIMAL(12,2) | NOT NULL, > 0 | Monto del abono en COP. Se valida que sea mayor a cero |
| `fecha` | DateTimeField | DATETIME | auto_now_add | Fecha y hora exacta del registro. Solo lectura |
| `notas` | CharField(255) | VARCHAR(255) | NULL, BLANK | Descripción opcional. Ej: "Quincena junio", "Premio trabajo" |

**Relación:** Una `MetaAhorro` puede tener muchos `Abono`. Un `Abono` pertenece a una sola `MetaAhorro`. (ForeignKey Many-to-One)

---

### 🗂 Diagrama de Relaciones entre Tablas

```
auth_user (Django nativo)
    │
    ├──[OneToOne]──► sena_perfil
    │                   - tipo_documento
    │                   - numero_documento (= auth_user.username)
    │                   - rol
    │                   - numero_ficha
    │
    └──[ForeignKey]──► sena_metaahorro
                            - nombre
                            - monto_objetivo
                            - monto_actual
                            - fecha_limite
                            │
                            └──[ForeignKey]──► sena_abono
                                                - cantidad
                                                - fecha
                                                - notas
```

---

## 🧠 Vistas y Lógica del Servidor

**Archivo:** `sena/views.py`

Todas las vistas están implementadas como **funciones** en Python (Function-Based Views). Cada vista maneja las peticiones HTTP `GET` (mostrar formulario/página) y `POST` (procesar datos enviados).

### `login_view`
- **GET:** Muestra el formulario de login con campos: tipo_documento, numero_documento, contraseña.
- **POST:** 
  1. Valida que tipo_documento sea CC, TI o CE.
  2. Valida que numero_documento no tenga caracteres especiales (regex: `^[a-zA-Z0-9]+$`).
  3. Valida que la contraseña tenga solo caracteres seguros.
  4. Autentica con Django usando `authenticate(username=numero, password=password)`.
  5. Si el usuario existe, **verifica que `perfil.tipo_documento == tipo_documento`** enviado.
  6. Si todo es correcto, inicia sesión y redirige al dashboard.
  7. Si algo falla, muestra mensaje de error específico.

### `registro_view`
- **GET:** Muestra el formulario de registro completo.
- **POST:** Crea un `User` de Django y un `Perfil` asociado. Valida: contraseñas iguales, documento único, caracteres permitidos.

### `dashboard`
- Requiere `@login_required`. Solo muestra la pantalla de novedades.

### `usuarios_view`
- Muestra la lista de usuarios con búsqueda y paginación.
- Si el rol es `aprendiz`, solo ve otros aprendices.
- Si el rol es `administrador`, ve todos y puede filtrar por rol.

### `metas_view`
- Muestra las metas del usuario autenticado.
- Calcula totales (objetivo, ahorrado, progreso general) con una sola consulta usando `aggregate()`.
- Pagina los resultados de 6 en 6.
- Las metas tienen acceso a sus abonos via `meta.abonos.all()` (related_name).

### `crear_meta`
- Solo acepta `POST`. Valida que la fecha límite no sea pasada.
- Crea el objeto `MetaAhorro` y redirige a la lista de metas.

### `actualizar_progreso_meta`
- Solo acepta `POST`. Valida que el monto sea > 0.
- Crea un objeto `Abono` con la cantidad, fecha automática y notas.
- Suma el monto al `monto_actual` de la meta y guarda.

### `editar_meta`
- Solo acepta `POST`. Valida fecha no pasada.
- Actualiza nombre, monto_objetivo y fecha_limite.

### `eliminar_meta`
- Solo acepta `POST`. Busca la meta del usuario y la borra (CASCADE borra sus abonos).

### `editar_usuario`
- Solo administradores. Valida duplicados de documento.
- Actualiza datos de `User` y `Perfil`. Gestiona permisos `is_staff`.

### `eliminar_usuario`
- Solo administradores. Impide que un admin se borre a sí mismo.

### `configuraciones_view`
- Maneja dos acciones vía campo oculto `action`:
  - `update_profile`: actualiza datos del perfil propio.
  - `change_password`: cambia la contraseña validando la actual. Mantiene la sesión activa.

### `logout_view`
- Solo acepta `POST` (método seguro contra CSRF). Cierra la sesión y redirige al login.

---

## 🌐 URLs y Rutas del Sistema

**Archivo:** `sena/urls.py`

| Método | URL | Vista | Descripción |
|--------|-----|-------|-------------|
| GET/POST | `/` | `login_view` | Redirige automáticamente al login |
| GET/POST | `/login/` | `login_view` | Formulario de inicio de sesión |
| GET/POST | `/registro/` | `registro_view` | Registro de nuevos usuarios |
| GET/POST | `/logout/` | `logout_view` | Cierra la sesión (POST requerido) |
| GET | `/dashboard/` | `dashboard` | Panel principal (requiere login) |
| GET | `/dashboard/usuarios/` | `usuarios_view` | Lista de usuarios (requiere login) |
| POST | `/dashboard/usuarios/editar/<id>/` | `editar_usuario` | Edita un usuario por ID de Perfil |
| POST | `/dashboard/usuarios/eliminar/<id>/` | `eliminar_usuario` | Elimina un usuario por ID de Perfil |
| GET | `/dashboard/metas/` | `metas_view` | Lista de metas de ahorro (requiere login) |
| POST | `/dashboard/metas/crear/` | `crear_meta` | Crea una nueva meta |
| POST | `/dashboard/metas/actualizar/<id>/` | `actualizar_progreso_meta` | Registra un abono a una meta |
| POST | `/dashboard/metas/editar/<id>/` | `editar_meta` | Edita una meta por ID |
| POST | `/dashboard/metas/eliminar/<id>/` | `eliminar_meta` | Elimina una meta por ID |
| GET/POST | `/dashboard/configuraciones/` | `configuraciones_view` | Configuraciones del perfil |

---

## 👥 Roles y Permisos

El sistema implementa un control de acceso basado en **dos roles** almacenados en el campo `Perfil.rol`:

### 🎓 Aprendiz (`rol = 'aprendiz'`)

| Módulo | Puede hacer |
|--------|-------------|
| Login | ✅ Iniciar sesión con su documento y contraseña |
| Metas | ✅ Ver, crear, editar, eliminar **sus propias** metas |
| Abonos | ✅ Registrar abonos a sus metas activas |
| Historial | ✅ Ver historial de abonos de cada una de sus metas |
| Usuarios | ✅ Ver la lista de **solo aprendices** (sin datos sensibles de admins) |
| Usuarios | ❌ No puede editar ni eliminar usuarios |
| Dashboard de novedades | ❌ No tiene acceso |
| Panel Django Admin | ❌ No tiene acceso |
| Configuraciones | ✅ Puede editar su propio perfil y cambiar su contraseña |

### 🛡️ Administrador (`rol = 'administrador'`)

| Módulo | Puede hacer |
|--------|-------------|
| Login | ✅ Iniciar sesión |
| Metas | ✅ Ver, crear, editar, eliminar **sus propias** metas |
| Usuarios | ✅ Ver **todos** los usuarios del sistema |
| Usuarios | ✅ Editar cualquier usuario (nombre, rol, documento, ficha) |
| Usuarios | ✅ Eliminar usuarios (excepto a sí mismo) |
| Usuarios | ✅ Filtrar usuarios por rol |
| Dashboard de novedades | ✅ Acceso al panel principal |
| Panel Django Admin | ✅ Acceso completo a `/admin/` |
| Configuraciones | ✅ Puede editar su propio perfil y cambiar su contraseña |

> **Implementación técnica:** El control de rol se verifica con la función auxiliar `obtener_rol_usuario(user)` que lee `user.perfil.rol`. Si el usuario es superusuario de Django sin perfil, se asume rol de administrador.

---

## 🎨 Diseño de la Interfaz

La interfaz fue diseñada con una estética **moderna y premium** usando las siguientes técnicas:

### Paleta de Colores
- **Color primario:** `#9d174d` (magenta oscuro — color institucional)
- **Color oscuro:** `#7a1040` (hover y sombras)
- **Color medio:** `#be185d` (gradientes)
- **Color de fondo:** `#f0f2f8` (gris muy claro)
- **Sidebar:** `#0d0d1f` (casi negro azulado)

### Componentes de Diseño

- **Cards de metas** con esquinas redondeadas (22px), sombras sutiles y animación de elevación al pasar el cursor (`translateY(-8px)`).
- **Header de cada meta** cambia de color según el estado: magenta (en progreso), verde (completada), rojo (vencida).
- **Barras de progreso** animadas con transición suave de 0.85 segundos y color según estado.
- **Sidebar** oscuro con íconos y texto. En móvil se colapsa a solo íconos (75px de ancho).
- **Modales** con bordes redondeados (20px), sin borde, con sombra elevada.
- **Animaciones de entrada** (fadeIn + translateY) para la carga inicial del contenido.
- **Inputs** con borde de color magenta al enfocarse, con sombra de brillo (`box-shadow: 0 0 0 3.5px rgba(157,23,77,.25)`).
- **Botones** con gradiente diagonal y efecto de elevación al hacer hover.

### Tipografía
- **Fuente:** `Outfit` de Google Fonts (pesos: 300, 400, 500, 600, 700, 800)
- Optimizada para legibilidad en pantallas digitales

### Responsividad
- En pantallas menores a 992px: el sidebar se minimiza a íconos.
- En pantallas menores a 768px: el sidebar oculta el texto de los elementos.
- La tarjeta de login oculta el panel de marca en móvil.

---

## 🔒 Seguridad Implementada

### Protecciones en el servidor (Backend)

1. **CSRF Token:** Todos los formularios `POST` incluyen `{% csrf_token %}`. Django verifica este token en cada petición POST para prevenir ataques Cross-Site Request Forgery.

2. **`@login_required`:** Todas las vistas del dashboard tienen este decorador. Si un usuario no autenticado intenta acceder, es redirigido al login automáticamente.

3. **Validación de rol:** Las vistas de edición/eliminación de usuarios verifican explícitamente que `rol_usuario == 'administrador'` antes de ejecutar cualquier acción.

4. **Validación de propiedad:** Al buscar una meta para abonar/editar/eliminar, siempre se filtra por `user=request.user`, impidiendo que un usuario manipule datos de otro (`MetaAhorro.objects.get(id=meta_id, user=request.user)`).

5. **Regex de validación en servidor:** Los campos de número de documento y contraseña se validan con expresiones regulares antes de procesar, incluso si el frontend ya los validó:
   - Documento: `^[a-zA-Z0-9]+$` (solo alfanumérico)
   - Contraseña: `^[a-zA-Z0-9!@#\$%\^\&\*\-_]+$` (alfanumérico + símbolos seguros)

6. **Validación de tipo de documento en login:** Se verifica que el tipo enviado coincida con el almacenado en el `Perfil` del usuario autenticado.

7. **Protección de auto-eliminación:** Un administrador no puede eliminar su propio usuario (`if user == request.user → error`).

8. **Validación de fechas en servidor:** Aunque el frontend limita el calendario, el servidor también rechaza fechas pasadas con un mensaje de error claro.

### Protecciones en el cliente (Frontend)

- Atributo `required` en todos los campos obligatorios.
- Atributo `pattern` con regex para el campo de número de documento.
- Atributo `min` dinámico en campos de fecha (se establece como la fecha de hoy via JavaScript).
- El botón de login se deshabilita al enviar el formulario para evitar doble envío.
- Confirmación con `confirm()` antes de eliminar metas o usuarios.

---

## ⚙️ Instalación Paso a Paso

Sigue estos pasos exactamente en orden para poner en marcha el proyecto desde cero.

### Paso 1 — Prerequisitos

Asegúrate de tener instalado en tu computador:

- ✅ **Python 3.11 o superior** → [python.org](https://www.python.org/downloads/)
- ✅ **XAMPP** (Apache + MySQL + phpMyAdmin) → [apachefriends.org](https://www.apachefriends.org/)
- ✅ **Git** (opcional, para clonar el repo) → [git-scm.com](https://git-scm.com/)
- ✅ **VS Code** o cualquier editor de código

### Paso 2 — Obtener el Proyecto

**Opción A — Con Git:**
```bash
git clone <url-del-repositorio>
cd djangoLilliana
```

**Opción B — Sin Git:**
Descomprime la carpeta del proyecto en tu ubicación preferida y ábrela con la terminal.

### Paso 3 — Crear el Entorno Virtual

El entorno virtual aísla las dependencias del proyecto del resto del sistema Python.

```bash
# Dentro de la carpeta djangoLilliana:
python -m venv env
```

**Activar el entorno virtual:**

```bash
# En Windows (PowerShell):
env\Scripts\Activate.ps1

# En Windows (CMD):
env\Scripts\activate.bat

# En Linux/Mac:
source env/bin/activate
```

> Sabrás que el entorno está activo porque verás `(env)` al inicio de tu terminal.

### Paso 4 — Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instala: Django, mysqlclient, python-dotenv y todas las dependencias necesarias.

### Paso 5 — Configurar XAMPP y MySQL

1. Abre el **Panel de Control de XAMPP**.
2. Inicia **Apache** y **MySQL** haciendo clic en "Start".
3. Abre tu navegador y entra a: `http://localhost/phpmyadmin`
4. En el menú izquierdo, haz clic en **"Nueva"** (o "New").
5. En el campo "Nombre de la base de datos" escribe: `sena`
6. En "Cotejamiento" selecciona: `utf8mb4_unicode_ci`
7. Haz clic en **"Crear"**.

### Paso 6 — Crear el Archivo de Entorno

En la raíz del proyecto (junto a `manage.py`), crea un archivo llamado exactamente **`.env`** con el siguiente contenido:

```env
SECRET_KEY=django-insecure-cambia-esta-clave-por-una-aleatoria-larga
DEBUG=True
DB_NAME=sena
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

> Si tu MySQL tiene contraseña, ponla en `DB_PASSWORD`. Por defecto en XAMPP la contraseña de root está vacía.

### Paso 7 — Aplicar las Migraciones

Este paso crea todas las tablas necesarias en la base de datos `sena`:

```bash
python manage.py migrate
```

Verás un output similar a:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sena, sessions
Running migrations:
  Applying sena.0001_initial... OK
  Applying sena.0002_metaahorro... OK
  Applying sena.0003_alter_perfil_rol... OK
  Applying sena.0004_abono... OK
  ...
```

### Paso 8 — Crear el Superusuario (Administrador Inicial)

```bash
python manage.py createsuperuser
```

El sistema te pedirá:
- **Username:** Escribe el número de documento del administrador (Ej: `12345678`)
- **Email:** Puedes dejarlo vacío o poner un email
- **Password:** Escribe una contraseña segura (mínimo 8 caracteres)
- **Password (again):** Repite la contraseña

Luego, necesitas crear el `Perfil` para este superusuario. Ve a `http://localhost:8000/admin/` → Perfiles → Añadir Perfil, y completa los datos.

---

## 🔑 Configuración de Variables de Entorno

El archivo `.env` contiene información sensible que **nunca debe subirse a Git**. Aquí se explica cada variable:

| Variable | Ejemplo | Descripción |
|----------|---------|-------------|
| `SECRET_KEY` | `django-insecure-abc123...` | Clave criptográfica de Django. Debe ser larga, aleatoria y única. Se usa para firmar sesiones y tokens CSRF |
| `DEBUG` | `True` | En desarrollo: `True` (muestra errores detallados). En producción: `False` |
| `DB_NAME` | `sena` | Nombre de la base de datos MySQL creada en phpMyAdmin |
| `DB_USER` | `root` | Usuario de MySQL. Por defecto en XAMPP es `root` |
| `DB_PASSWORD` | *(vacío)* | Contraseña de MySQL. En XAMPP local suele estar vacía |
| `DB_HOST` | `localhost` | Dirección del servidor MySQL. En local siempre es `localhost` |
| `DB_PORT` | `3306` | Puerto de MySQL. El puerto estándar es `3306` |

**Generar una SECRET_KEY segura:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🗃 Base de Datos en phpMyAdmin

La base de datos `sena` contiene exactamente **13 tablas** necesarias para el proyecto Django:

### Tablas de tu aplicación Django (`sena/`)

| Tabla | Modelo | Descripción |
|-------|--------|-------------|
| `sena_perfil` | `Perfil` | Datos de perfil extendidos de los usuarios |
| `sena_metaahorro` | `MetaAhorro` | Metas de ahorro de cada usuario |
| `sena_abono` | `Abono` | Historial de pagos por meta |

### Tablas del sistema de autenticación de Django

| Tabla | Descripción |
|-------|-------------|
| `auth_user` | Usuarios registrados (username=numero_documento, password hasheada) |
| `auth_group` | Grupos de permisos (no se usa activamente en este proyecto) |
| `auth_permission` | Permisos disponibles en el sistema |
| `auth_user_groups` | Relación usuarios-grupos |
| `auth_user_user_permissions` | Permisos individuales por usuario |
| `auth_group_permissions` | Permisos por grupo |

### Tablas internas de Django

| Tabla | Descripción |
|-------|-------------|
| `django_admin_log` | Historial de acciones realizadas desde el panel `/admin/` |
| `django_content_type` | Registro de modelos del sistema (usado por permisos y admin) |
| `django_migrations` | Registro de migraciones ya aplicadas (evita duplicados) |
| `django_session` | Sesiones activas de usuarios logueados |

> ⚠️ **Importante:** Nunca elimines las tablas de Django (`auth_*` y `django_*`). Son esenciales para el funcionamiento del framework.

---

## ▶️ Cómo Ejecutar el Proyecto

### Iniciar el servidor de desarrollo

```bash
# Asegúrate de que el entorno virtual esté activo (verás "(env)" en la terminal)
# Asegúrate de que XAMPP esté corriendo (Apache + MySQL)

python manage.py runserver
```

Verás:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 22, 2026 - 21:00:00
Django version 5.x, using settings 'mi_proyecto.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Acceder al sistema

| URL | Descripción |
|-----|-------------|
| `http://127.0.0.1:8000/` | Página principal (redirige al login) |
| `http://127.0.0.1:8000/login/` | Formulario de inicio de sesión |
| `http://127.0.0.1:8000/registro/` | Registro de nuevo usuario |
| `http://127.0.0.1:8000/dashboard/metas/` | Módulo de metas de ahorro |
| `http://127.0.0.1:8000/admin/` | Panel de administración de Django |

### Detener el servidor

Presiona `Ctrl + C` en la terminal donde corre el servidor.

---

## 🔧 Panel de Administración Django

El panel de administración en `/admin/` es una interfaz automática de Django que permite gestionar los datos directamente desde el navegador sin escribir SQL.

**¿Cómo acceder?**
1. Corre el servidor: `python manage.py runserver`
2. Abre: `http://127.0.0.1:8000/admin/`
3. Inicia sesión con el superusuario creado en el Paso 8.

**¿Qué puedes hacer en el panel admin?**

| Sección | Acciones disponibles |
|---------|---------------------|
| **Perfiles** | Ver, crear, editar y eliminar perfiles. Filtrar por rol y tipo de documento. Buscar por nombre o número de documento. |
| **Metas de Ahorro** | Ver todas las metas de todos los usuarios. Ver el estado calculado de cada meta. |
| **Abonos** | Ver el historial completo de abonos de todo el sistema. Filtrar por fecha y usuario. |
| **Usuarios (auth)** | Gestión de cuentas de usuario a bajo nivel. |

---

## 📦 Dependencias del Proyecto

**Archivo:** `requirements.txt`

```
Django>=5.0
mysqlclient>=2.1.0
python-dotenv>=1.0.0
```

**Descripción de cada dependencia:**

| Paquete | Para qué sirve |
|---------|---------------|
| `Django` | El framework completo: ORM, vistas, templates, autenticación, admin, migraciones, servidor de desarrollo |
| `mysqlclient` | Driver de conexión entre Django y MySQL. Requiere las librerías de desarrollo de MySQL instaladas en el sistema |
| `python-dotenv` | Lee las variables del archivo `.env` y las carga como variables de entorno al inicio del proyecto |

**Dependencias incluidas en Django (no requieren instalación separada):**
- `django.contrib.humanize` → Filtro `intcomma` para formatear números (1500000 → 1,500,000)
- `django.contrib.auth` → Sistema de autenticación, usuarios, grupos y permisos
- `django.contrib.admin` → Panel de administración automático

---

## 🔄 Flujo Completo de la Aplicación

Este diagrama describe el recorrido de un usuario típico a través del sistema:

```
[Usuario abre el navegador]
         │
         ▼
  http://localhost:8000/
         │ (redirige)
         ▼
  ┌─────────────────┐
  │   LOGIN PAGE    │ ← Ingresa: Tipo doc + Número + Contraseña
  └────────┬────────┘
           │ POST → login_view valida:
           │  1. Tipo doc válido (CC/TI/CE)
           │  2. Formato de documento correcto
           │  3. Credenciales correctas en auth_user
           │  4. Tipo doc coincide con sena_perfil
           │
           ▼
  ┌─────────────────────┐
  │   DASHBOARD         │ ← Sidebar con navegación
  │  (si es admin)      │
  └────────┬────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
[METAS]       [USUARIOS]
    │
    ├── Ver mis metas (grid paginado)
    ├── Buscar meta por nombre
    ├── [Nueva Meta] → Modal: nombre, monto, fecha
    │       └─► POST crear_meta → valida fecha → guarda en sena_metaahorro
    │
    ├── [Registrar Abono] (solo metas activas)
    │       └─► Modal: cantidad + notas
    │               └─► POST actualizar_progreso_meta
    │                       → crea registro en sena_abono
    │                       → suma monto a sena_metaahorro.monto_actual
    │
    ├── [Ver Historial] (todas las metas)
    │       └─► Modal con tabla de abonos de esa meta
    │               Datos: meta.abonos.all() (cargados en el HTML)
    │               JS parsea data-abonos JSON y renderiza tabla
    │
    ├── [⋮ Menú] → Editar Meta
    │       └─► Modal: editar nombre, monto, fecha → POST editar_meta
    │
    └── [⋮ Menú] → Eliminar Meta
            └─► confirm() → POST eliminar_meta → borra meta + sus abonos (CASCADE)
```

---

## 📝 Notas para el Desarrollador

### Cómo agregar un nuevo modelo

1. Define la clase en `sena/models.py`.
2. Corre: `python manage.py makemigrations sena`
3. Aplica: `python manage.py migrate`
4. Registra en `sena/admin.py` con `@admin.register(TuModelo)`.

### Cómo agregar una nueva página/vista

1. Crea la función en `sena/views.py`.
2. Agrega la ruta en `sena/urls.py`.
3. Crea el template HTML en `sena/templates/`.
4. Si usa el dashboard, extiende `base_dashboard.html` con `{% extends 'base_dashboard.html' %}`.

### Cómo agregar estáticos locales nuevos

1. Coloca el archivo en `sena/static/sena/css/` o `sena/static/sena/js/`.
2. En el template: `{% load static %}` y luego `{% static 'sena/css/archivo.css' %}`.
3. Si es producción, corre: `python manage.py collectstatic`.

### Sobre el sistema de templates

El proyecto usa el sistema de **herencia de templates** de Django:

```
base_dashboard.html          ← Define bloques: title, extra_css, content, modals, extra_js
    ├── dashboard.html        ← {% extends 'base_dashboard.html' %}
    ├── metas.html            ← {% extends 'base_dashboard.html' %}
    ├── usuarios.html         ← {% extends 'base_dashboard.html' %}
    └── configuraciones.html  ← {% extends 'base_dashboard.html' %}

login.html                   ← Template standalone (no extiende nada)
registro.html                ← Template standalone (no extiende nada)
```

### Generación del número de documento como username

En este sistema, el **número de documento es el `username`** de Django:
- Al registrarse: `User.objects.create_user(username=numero_documento, ...)`
- Al hacer login: `authenticate(request, username=numero_documento, password=...)`
- Esto significa que el número de documento debe ser **único** en todo el sistema.

---

*Proyecto formativo SENA — Gestión de Finanzas · Desarrollado en 2026*  
*Stack: Python · Django · MySQL · Bootstrap 5 · JavaScript*
