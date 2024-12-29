from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True

INTERNAL_IPS = []

ALLOWED_HOSTS = ["*"]

# LiqPay Api
LIQPAY_PUBLIC_KEY = os.getenv("LIQPAY_PUBLIC_KEY")
LIQPAY_PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

INSTALLED_APPS = [
    "jazzmin",
    "django_ckeditor_5",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "rosetta",
    # Payments
    "liqpay",
    "catalog",
    "users",
    "info",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "templates" / "pages",
            BASE_DIR / "templates" / "elements",
        ],
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

WSGI_APPLICATION = "settings.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "uk-uk"

TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("uk", "Українська"),
    ("ru", "Російська"),
]

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / ".."
STATICFILES_DIRS = [
    STATIC_ROOT / "static",
]

MEDIA_URL = "media/"
MEDIA_ROOT = STATIC_ROOT / "static" / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",  # Добавляем заголовки (H1, H2 и т.д.)
            "|",
            "bold",  # Жирный текст
            "italic",  # Курсив
            "underline",  # Подчеркивание
            "fontColor",  # Цвет текста
            "fontBackgroundColor",  # Цвет фона текста
        ],
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "fontColor": {
            "colors": [
                {"color": "hsl(0, 0%, 0%)", "label": "Black"},
                {"color": "hsl(0, 75%, 60%)", "label": "Red"},
                {"color": "hsl(30, 75%, 60%)", "label": "Orange"},
                {"color": "hsl(60, 75%, 60%)", "label": "Yellow"},
                {"color": "hsl(120, 75%, 60%)", "label": "Green"},
                {"color": "hsl(180, 75%, 60%)", "label": "Turquoise"},
                {"color": "hsl(240, 75%, 60%)", "label": "Blue"},
                {"color": "hsl(300, 75%, 60%)", "label": "Purple"},
            ]
        },
        "fontBackgroundColor": {
            "colors": [
                {"color": "hsl(0, 0%, 100%)", "label": "White"},
                {"color": "hsl(0, 75%, 60%)", "label": "Red"},
                {"color": "hsl(30, 75%, 60%)", "label": "Orange"},
                {"color": "hsl(60, 75%, 60%)", "label": "Yellow"},
                {"color": "hsl(120, 75%, 60%)", "label": "Green"},
                {"color": "hsl(180, 75%, 60%)", "label": "Turquoise"},
                {"color": "hsl(240, 75%, 60%)", "label": "Blue"},
                {"color": "hsl(300, 75%, 60%)", "label": "Purple"},
            ]
        },
        "language": "uk",
    }
}
