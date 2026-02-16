from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
from users.defaults import ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == 'True'
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1").split(",")


# Application definition
INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    
    # apps
    'users',
    'listing',
    
    # tools
    'phonenumber_field',
    'django_filters',
    'corsheaders',
    'drf_yasg',   
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car_marketplace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'car_marketplace.wsgi.application'
AUTH_USER_MODEL = "users.User"

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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


# Restframework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "users.authentications.CookieJWTAuthentication",
    ),
    "COERCE_DECIMAL_TO_STRING": False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=ACCESS_TOKEN_LIFETIME),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME),
}


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redis Configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1"), 
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

MEDIA_URL = '/media/'
MEDIA_ROOT = './media'

STATIC_URL = '/static/'
STATIC_ROOT = '/app/static'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",  
]
# Silence Swagger warning
SWAGGER_USE_COMPAT_RENDERERS = False