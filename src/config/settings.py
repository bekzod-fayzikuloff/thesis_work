import os
from datetime import timedelta
from pathlib import Path
from typing import TypeVar

from dotenv import load_dotenv

from .env import database_config

load_dotenv("./envs/.env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", 0)))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")


# Application definition

Package = TypeVar("Package", bound=str)
PackagesListType = list[Package]

THIRD_PARTY_PACKAGES: PackagesListType = [
    "corsheaders",
    "rest_framework",
    "django_celery_results",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework_simplejwt",
    "channels",
    "django_filters",
]

PROJECT_APPS: PackagesListType = [
    "apps.api", "apps.chats", "apps.posts", "apps.authentication", "apps.profiles", "apps.calls"
]

INSTALLED_APPS = [
    "daphne",
    "jazzmin",  # THIRD_PARTY_PACKAGE for customize admin panel
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_PACKAGES,
    *PROJECT_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

############
# CHANNELS #
############
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}


############
# Database #
############
DATABASES = {"default": database_config.get(os.environ.get("MODE"))}

##################
# REST_FRAMEWORK #
##################
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        # Any other renders
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    'DEFAULT_PARSER_CLASSES': (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework_xml.parsers.XMLParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser'
        # Any other parsers
    )
}

JSON_CAMEL_CASE = {
    'RENDERER_CLASS': 'rest_framework.renderers.JSONRenderer'
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
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
AUTH_USER_MODEL = "authentication.User"

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


########
# CORS #
########

CORS_ORIGIN_ALLOW_ALL = bool(int(os.environ.get("CORS_ORIGIN_ALLOW_ALL", 0)))

CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST").split(",")

#############
# SIMPLEJWT #
#############
SIMPLE_JWT_SIGNING_KEY = os.environ.get("SIMPLE_JWT_SIGNING_KEY")


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SIMPLE_JWT_SIGNING_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


##########
# CELERY #
##########
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {}


###############
# DOCS_SCHEMA #
###############
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    }
}

DOCS_SCHEMA_TITLE = os.environ.get("DOCS_SCHEMA_TITLE")
DOCS_SCHEMA_DESCRIPTION = os.environ.get("DOCS_SCHEMA_DESCRIPTION")
DOCS_SCHEMA_VERSION = os.environ.get("DOCS_SCHEMA_VERSION")
DOCS_SCHEMA_TERMS_OF_SERVICE = os.environ.get("DOCS_SCHEMA_TERMS_OF_SERVICE")
DOCS_SCHEMA_CONTACT_EMAIL = os.environ.get("DOCS_SCHEMA_CONTACT_EMAIL")
DOCS_SCHEMA_LICENSE = os.environ.get("DOCS_SCHEMA_LICENSE")
DOCS_SCHEMA_PUBLIC = bool(int(os.environ.get("DOCS_SCHEMA_PUBLIC", '0')))

SPECTACULAR_SETTINGS = {
    "TITLE": DOCS_SCHEMA_TITLE,
    "DESCRIPTION": DOCS_SCHEMA_DESCRIPTION,
    "VERSION": DOCS_SCHEMA_VERSION,
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    'CAMELIZE_NAMES': True,
    'POSTPROCESSING_HOOKS': ['drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields'],
}


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Thesis Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Thesis",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Thesis",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "unwind_logo_mini.png",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "unwind_logo_mini.png",
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the thesis",
    # Copyright on the footer
    "copyright": "fayzikuloff.b@gmail.com",
    "search_model": AUTH_USER_MODEL,
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Falcon", "url": "https://example.com", "new_window": True},
        {"app": "profiles"},
        {"app": "chats"},
        {"app": "posts"},
        # external url that opens in a new window (Permissions can be added)
        #
        # model admin to link to (Permissions checked against model)
        # App with dropdown menu to all its models pages (Permissions checked against models)
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["authentication", "profiles", "posts", "chats"],
    "icons": {
        "authentication": "fas fa-users-cog",
        "authentication.user": "fas fa-user",
        #
        "profiles.profile": "fas fa-user",
        "profiles.follower": "fas fa-light fa-people-arrows",
        #
        "posts.postsgroup": "fas fa-regular fa-layer-group",
        "posts.postmedia": "fas fa-duotone fa-images",
        "posts.post": "fas fa-duotone fa-plus",
        "posts.comment": "fas fa-sharp fa-solid fa-comment-dots",
        "posts.reaction": "fas fa-regular fa-thumbs-up",
        #
        "chats.chat": "fas fa-regular fa-spa",
        "chats.privatechat": "fas fa-duotone fa-plus",
        "chats.media": "fas fa-duotone fa-images",
        "chats.message": "fas fa-regular fa-envelope",
        "chats.elected": "fas fa-duotone fa-check-double"

    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

# Насторойка визуальной части админ панели
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-lightblue",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
    "actions_sticky_top": False,
}
