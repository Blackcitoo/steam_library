# Guía de Instalación Rápida

## Instalación Local (Recomendado para desarrollo)

### 1. Requisitos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### 2. Pasos de Instalación

```bash
# 1. Navegar al directorio del proyecto
cd steam_library

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno (opcional)
# Copiar .env.example a .env y editar si es necesario
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# 6. Ejecutar migraciones
python manage.py migrate

# 7. Crear superusuario (opcional)
python manage.py createsuperuser

# 8. Cargar datos de ejemplo (opcional)
python manage.py create_sample_data

# 9. Ejecutar servidor
python manage.py runserver
```

### 3. Acceder a la Aplicación

- **Aplicación**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

## Instalación con Docker

### 1. Requisitos
- Docker
- Docker Compose

### 2. Pasos

```bash
# 1. Navegar al directorio del proyecto
cd steam_library

# 2. Construir y ejecutar
docker-compose up --build

# 3. En otra terminal, crear superusuario
docker-compose exec web python manage.py createsuperuser

# 4. Cargar datos de ejemplo (opcional)
docker-compose exec web python manage.py create_sample_data
```

### 3. Acceder

- **Aplicación**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

## Usuarios de Prueba

Después de ejecutar `create_sample_data`, puedes usar:

- **Admin**: username: `admin`, password: `admin123`
- **Usuario**: username: `usuario1`, password: `usuario123`

## Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Error: "Database is locked"
Cerrar todas las conexiones y reiniciar el servidor.

### Error: "Static files not found"
```bash
python manage.py collectstatic
```

### Error: "Migration conflicts"
```bash
python manage.py makemigrations
python manage.py migrate
```

