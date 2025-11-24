"""
Django settings for Swap Admin Service.
"""

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-not-for-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,admin').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration - Multi-database support
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'admin',
        'USER': os.getenv('DB_USER', 'swap_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'swap_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'auth_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auth',
        'USER': os.getenv('DB_USER', 'swap_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'swap_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'users_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'users',
        'USER': os.getenv('DB_USER', 'swap_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'swap_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'listings_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'listings',
        'USER': os.getenv('DB_USER', 'swap_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'swap_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'offers_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'offers',
        'USER': os.getenv('DB_USER', 'swap_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'swap_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'payments_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'payments',
        'USER': os.getenv('DB_USER', 'swap_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'swap_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'chat_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chat',
        'USER': os.getenv('DB_USER', 'swap_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'swap_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'notifications_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'notifications',
        'USER': os.getenv('DB_USER', 'swap_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'swap_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# CORS configuration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8001',
    'http://localhost:8002',
    'http://localhost:8003',
    'http://localhost:8004',
    'http://localhost:8005',
    'http://localhost:8006',
    'http://localhost:8007',
    'http://localhost:8008',
    'http://127.0.0.1:3000',
]

# Admin site customization
ADMIN_TITLE = 'Swap Platform Administration'
ADMIN_HEADER = 'Swap Admin Dashboard'
