# bolsa_trabajo/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicaciones propias
    'usuarios',
    'perfiles',
    'vacantes',
    'postulaciones',
    'core',
    
    # Aplicaciones de terceros
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# Configuración de la base de datos

# bolsa_trabajo/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bolsa_trabajo',
        'USER': 'bolsa_admin',
        'PASSWORD': '//BT29042025&&',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# bolsa_trabajo/settings.py

AUTH_USER_MODEL = 'usuarios.Usuario'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
