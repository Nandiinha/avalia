import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Identificar o ambiente
ENVIRONMENT = os.getenv("DJANGO_ENV", "development")

# Configuração padrão para desenvolvimento
IS_DEVELOPMENT = ENVIRONMENT == "development"

# Configurar a porta do Django
DJANGO_PORT = os.getenv("DJANGO_PORT", "8000")

# Configuração do DEBUG
DEBUG = os.getenv("DEBUG", "False") == "True" if not IS_DEVELOPMENT else True

# Configurar ALLOWED_HOSTS com base no ambiente
ALLOWED_HOSTS = (
    os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if not IS_DEVELOPMENT
    else ["127.0.0.1", "localhost"]
)

# Segurança
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-development-key" if IS_DEVELOPMENT else None,
)
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não definido para produção!")

# Banco de Dados
DB_SQLLITE_PATH = os.getenv("DB_SQLLITE_PATH", os.path.join(BASE_DIR, "db.sqlite3"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DB_SQLLITE_PATH,
    }
}

# Logar o ambiente de execução
logger.info(f"App Log - Ambiente de execução: {'Desenvolvimento' if IS_DEVELOPMENT else 'Produção'}")

# Verificar se o arquivo do banco de dados existe e logar o caminho
if os.path.exists(DB_SQLLITE_PATH):
    logger.info(f"App Log - Usando banco de dados existente em: {DB_SQLLITE_PATH}")
else:
    logger.warning(
        f"App Log - O banco de dados não existe. Será criado em: {DB_SQLLITE_PATH}"
    )

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "correction",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Middleware para servir arquivos estáticos em produção
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "TCC.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "TCC.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = (
    [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]
    if not IS_DEVELOPMENT
    else []
)

# Backend personalizado
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "correction.backends.EmailBackend",
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "correction" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise para arquivos estáticos em produção
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if not IS_DEVELOPMENT
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuração adicional para Vercel
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1,http://localhost" if IS_DEVELOPMENT else "",
).split(",")

# Logging adicional
logger.info(f"App Log - Servidor Django configurado para rodar na porta {DJANGO_PORT}")
logger.info(f"App Log - Caminho do banco de dados configurado: {DB_SQLLITE_PATH}")
logger.info(f"App Log - Valor de DEBUG: {DEBUG}")
