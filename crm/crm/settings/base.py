import os

from . import BASE_DIR

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(',')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "easy_thumbnails",
    "htmx",
    "file_downloader.apps.FileDownloaderConfig",
    "tables.apps.TablesConfig",
    "patients.apps.PatientsConfig",
    "users.apps.UsersConfig",
    "hospitalizations.apps.HospitalizationsConfig",
    "dynamic_breadcrumbs.apps.BreadcrumbingConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "crm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "patients.context_processors.get_patients_context",
                "dynamic_breadcrumbs.context_processors.breadcrumbs",
            ],
        },
    },
]

WSGI_APPLICATION = "crm.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Logging
DJANGO_LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "ERROR")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s %(levelname)-8s %(asctime)s %(module)s "
            "%(reset)s %(blue)s%(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
        "file": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": "debug.log",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        },
    },
}

# CRM Settings
PATIENTS_PAGINATE_BY = 10

LOGIN_REDIRECT_URL = "patients:index"
LOGOUT_REDIRECT_URL = "users:login"
LOGIN_URL = "users:login"

AUTH_USER_MODEL = "users.User"

DEFAULT_USER_IMAGE = MEDIA_URL + "users/noun-profile-801396.png"

AVATAR_FILE_MAX_SIZE = 1000 * 256  # kibibytes
AVATAR_MAX_WIDTH = 600
AVATAR_MIN_WIDTH = 100
AVATAR_MAX_HEIGHT = 600
AVATAR_MIN_HEIGHT = 100
AVATAR_WIDTH = 150
AVATAR_HEIGHT = 150

# Celery
BROKER_HOSTPORT = os.environ.get("BROKER_HOSTPORT")
BROKER_PORT = os.environ.get("BROKER_PORT")
RABBITMQ_DEFAULT_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_NAME = os.environ.get("REDIS_NAME")


# Breadcrumbs
DYNAMIC_BREADCRUMBS_PATH_MAX_DEPTH = 10
DYNAMIC_BREADCRUMBS_HOME_LABEL = "Главная"
DYNAMIC_BREADCRUMBS_SHOW_VERBOSE_NAME = True
DYNAMIC_BREADCRUMBS_URLS_NAMES = {
    "documents": "Документы",
    "add": "Добавление госпитализации",
    "update": "Редактирование госпитализации",
    "leave": "Выписать",
    "current": "Находящиеся на лечении",
    "about": "О проекте",
    "contacts": "Контакты",
}
DYNAMIC_BREADCRUMBS_EXCLUDE = ("sort",)
DYNAMIC_BREADCRUMBS_SHOW_ID = False
