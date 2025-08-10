import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== Config por entorno (.env) =====
DEBUG = os.getenv('DEBUG', '1') == '1'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-inseguro-cambia-esto')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ===== Apps =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MemoryGameMVC',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MemoryGame.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # opcional: además de templates en apps
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MemoryGame.wsgi.application'

# ===== Base de datos (MySQL vía variables de entorno) =====
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB', 'memorygame_db'),
        'USER': os.getenv('MYSQL_USER', 'memoryuser'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'super_segura'),
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),  # en Docker: "db"
        'PORT': os.getenv('MYSQL_PORT', '3306'),       # en Docker: 3306 interno
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# ===== Password validators =====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===== Internacionalización =====
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Tegucigalpa'
USE_I18N = True
USE_TZ = True

# ===== Archivos estáticos =====
STATIC_URL = 'static/'
# Si tienes una carpeta 'static' a nivel proyecto, descomenta:
# STATICFILES_DIRS = [BASE_DIR / 'static']
# Para producción usarías STATIC_ROOT, pero en dev no hace falta.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Autenticación: usa nuestras rutas
LOGIN_URL = 'login'            # nombre de la URL de login (path('login/', ... name='login'))
LOGIN_REDIRECT_URL = 'home'    # a dónde ir después de iniciar sesión
LOGOUT_REDIRECT_URL = 'login'  # a dónde ir después de cerrar sesión

