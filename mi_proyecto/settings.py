"""
Django settings for mi_proyecto project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from django.conf.urls import handler404, handler500
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=hi+$fr1_n8bho18zg4iwlwic-k&d3kh90h+5%-px2-^&1*k&2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'tu_dominio.com']



# Application definition

INSTALLED_APPS = [    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'usuarios',
    'parametria',
    'habilitadores',
    'habilitadores_iniciativa',
    'crispy_forms',
     'axes',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mi_proyecto.middleware.session_timeout_middleware.SessionTimeoutMiddleware',
    'axes.middleware.AxesMiddleware',     
]

ROOT_URLCONF = 'mi_proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Agrega aquí la ruta a tus templates globales, si los tienes
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



WSGI_APPLICATION = 'mi_proyecto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'BD_Proyecto',
        'USER': 'sa',
        'PASSWORD': '$inteco2207$',
        'HOST': 'NTB-CND127GZTQ\\SQLEXPRESS',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

#cadena de configuracion con keyvalue
#instalar pip install azure-identity azure-keyvault-secrets



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Backend de Axes
    'django.contrib.auth.backends.ModelBackend',  # Backend de autenticación predeterminado de Django
]



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# settings.py
X_FRAME_OPTIONS = 'DENY'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Asegúrate de que esta carpeta realmente exista
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Esta carpeta se usará cuando ejecutes 'collectstatic'



CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Configuración para Jira
JIRA_EMAIL = 'inteco2207@gmail.com'
JIRA_API_TOKEN = 'ATATT3xFfGF0_7dg6e9Z52MuOCc4clVtUvuaXJ9xWYDp27sHdKiOTgvOITw65GlujMjfHev-Zsphe3wtObJJvc_u3zMVz-kcbIlRiJ_lOz7GUFlNtWUWY4ghUPIr7rL42G9vpngqHUzxtyl6ixbX9IsUp8rl5rPAOI1i_qLXee_tLj4dbVZ3QyA=667CE1A3'



# Define una clave secreta para itsdangerous
ITS_DANGEROUS_SECRET_KEY = 'tu_clave_secreta_segura'  # Cambia 'tu_clave_secreta_segura' por una cadena única y segura

#handler404 = 'mi_proyecto.views.error_404'
#handler500 = 'mi_proyecto.views.error_500'

DEBUG = True


# Configuración de seguridad de Django Axes
AXES_FAILURE_LIMIT = 5  # Número de intentos fallidos antes de bloquear
AXES_COOLOFF_TIME = 1  # Tiempo en horas que el usuario estará bloqueado
AXES_LOCK_OUT_AT_FAILURE = True  # Bloquear después de alcanzar el límite de intentos fallidos
AXES_RESET_ON_SUCCESS = True  # Reiniciar los intentos fallidos después de un inicio de sesión exitoso
AXES_USERNAME_FORM_FIELD = 'username'  # Campo de formulario utilizado para el nombre de usuario











