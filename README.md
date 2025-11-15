# 🎮 Biblioteca de Steam - Proyecto Django

Sistema completo de gestión de biblioteca de juegos de Steam desarrollado con Django, que permite a los usuarios gestionar su colección de juegos, escribir reseñas, y explorar catálogos de juegos.

## 📋 Características

### Funcionalidades Principales
- ✅ **Sistema de Autenticación Completo**: Registro, login, logout con usuarios personalizados
- ✅ **CRUD Completo**: Gestión de Juegos y Reseñas con Class-Based Views
- ✅ **Biblioteca Personal**: Cada usuario puede gestionar su propia biblioteca de juegos
- ✅ **Sistema de Reseñas**: Los usuarios pueden calificar y comentar juegos
- ✅ **Búsqueda Avanzada**: Búsqueda por título, descripción, desarrollador y filtros
- ✅ **Paginación**: Implementada en todas las listas
- ✅ **Notificaciones**: Sistema de notificaciones para usuarios
- ✅ **Exportar Datos**: Exportación de biblioteca a CSV
- ✅ **API REST Completa**: API RESTful con Django REST Framework
- ✅ **Admin Personalizado**: Panel de administración completamente personalizado
- ✅ **Diseño Responsive**: Interfaz adaptada para móvil y desktop con Bootstrap 5

### Modelos Implementados
1. **User**: Usuario personalizado con biografía, avatar, perfil de Steam
2. **Game**: Juegos con título, descripción, precio, desarrollador, categorías
3. **Developer**: Desarrolladores de juegos
4. **Category**: Categorías de juegos
5. **UserLibrary**: Biblioteca personal de cada usuario
6. **Review**: Reseñas y calificaciones de juegos
7. **Notification**: Sistema de notificaciones

## 🚀 Instalación

### Requisitos Previos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Instalación Local

1. **Clonar o descargar el proyecto**
```bash
cd steam_library
```

2. **Crear un entorno virtual (recomendado)**
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones (opcional para desarrollo)
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

7. **Cargar datos de ejemplo (opcional)**
```bash
python manage.py loaddata fixtures/initial_data.json
```

8. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

9. **Acceder a la aplicación**
- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

### Instalación con Docker

1. **Construir y ejecutar con Docker Compose**
```bash
docker-compose up --build
```

2. **Crear superusuario**
```bash
docker-compose exec web python manage.py createsuperuser
```

3. **Acceder a la aplicación**
- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 👥 Usuarios de Prueba

### Usuario Administrador
- **Username**: gamer
- **Password**: gamer123
- **Permisos**: Acceso completo al sistema y panel de administración

### Usuario Regular
- **Username**: Tranqui静寂
- **Password**: desarrollo111
- **Permisos**: Usuario estándar con acceso a biblioteca y reseñas

### Crear Usuarios de Prueba

```bash
python manage.py shell
```

```python
from library.models import User

# Crear usuario admin
admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
admin.is_staff = True
admin.save()

# Crear usuario regular
user = User.objects.create_user('usuario1', 'usuario1@example.com', 'usuario123')
```

## 📁 Estructura del Proyecto

```
steam_library/
├── manage.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── README.md
├── steam_library/          # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── library/                # Aplicación principal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── serializers.py
│   ├── api_views.py
│   ├── api_urls.py
│   ├── tests.py
│   └── migrations/
├── templates/              # Templates HTML
│   ├── base.html
│   └── library/
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── game_list.html
│       ├── game_detail.html
│       ├── game_form.html
│       ├── my_library.html
│       ├── review_form.html
│       ├── developer_list.html
│       ├── developer_detail.html
│       ├── user_profile.html
│       └── notifications.html
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── media/                  # Archivos subidos por usuarios
└── db.sqlite3             # Base de datos (SQLite para desarrollo)
```

## 🔧 Configuración

### Variables de Entorno

El proyecto usa variables de entorno para configuración sensible. Crea un archivo `.env` basado en `.env.example`:

- `SECRET_KEY`: Clave secreta de Django (cambiar en producción)
- `DEBUG`: Modo debug (False en producción)
- `ALLOWED_HOSTS`: Hosts permitidos (separados por comas)

### Base de Datos

Por defecto, el proyecto usa SQLite para desarrollo. Para producción, se recomienda PostgreSQL:

```python
# En settings.py, cambiar DATABASES para usar PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'steam_library',
        'USER': 'steam_user',
        'PASSWORD': 'steam_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

Ejecutar tests:

```bash
python manage.py test
```

Ejecutar tests con coverage:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML en htmlcov/
```

## 📡 API REST

El proyecto incluye una API REST completa. Documentación disponible en:

- **Base URL**: http://127.0.0.1:8000/api/
- **Endpoints principales**:
  - `/api/games/` - Lista y creación de juegos
  - `/api/reviews/` - Lista y creación de reseñas
  - `/api/library/` - Biblioteca del usuario autenticado
  - `/api/developers/` - Lista de desarrolladores
  - `/api/categories/` - Lista de categorías



## 🎨 Características de Diseño

- **Bootstrap 5**: Framework CSS moderno y responsive
- **Tema Steam**: Colores inspirados en Steam (azul oscuro, azul claro)
- **Iconos Bootstrap Icons**: Iconos modernos y consistentes
- **Responsive Design**: Adaptado para móvil, tablet y desktop
- **UX Optimizada**: Navegación intuitiva y feedback visual

## 🔐 Seguridad

- Autenticación de usuarios con Django Auth
- Protección CSRF en todos los formularios
- Validación de permisos en vistas (solo staff puede crear/editar juegos)
- Validación de formularios con Django Forms
- Passwords hasheados (no se almacenan en texto plano)

## 📊 Funcionalidades Extra Implementadas

- ✅ **Class-Based Views** (+5): Todas las vistas CRUD usan CBV
- ✅ **Paginación** (+3): Implementada en listas de juegos, reseñas, biblioteca
- ✅ **Búsqueda Avanzada** (+5): Búsqueda por múltiples campos y filtros
- ✅ **Notificaciones** (+5): Sistema completo de notificaciones
- ✅ **Exportar CSV** (+5): Exportación de biblioteca a CSV
- ✅ **API REST Completa** (+10): API RESTful con DRF
- ✅ **Tests (coverage >50%)** (+10): Suite completa de tests
- ✅ **Docker** (+10): Dockerfile y docker-compose.yml

## Miembros del Equipo

1. Benitez Victor
2. Cardozo Rodrigo
3. Gimenez Fabrizzio
4. Medina Esteban

## 📝 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar servidor
python manage.py runserver

# Ejecutar tests
python manage.py test

# Abrir shell de Django
python manage.py shell
```

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Error: "Database is locked" (SQLite)
- Cerrar todas las conexiones a la base de datos
- Reiniciar el servidor de desarrollo

### Error: "Static files not found"
```bash
python manage.py collectstatic
```

### Error: "Migration conflicts"
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📄 Licencia

Este proyecto es un proyecto educativo desarrollado para fines académicos.

## 👤 Autor

Proyecto desarrollado como Proyecto Integrador Django.



**¡Gracias por usar Biblioteca de Steam!** 🎮



