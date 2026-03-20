from .base import *  # noqa
from .base import env
from .base import ROOT_DIR

import os

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405

SECRET_KEY = "not-secret-whatsoever"  # noqa: S105 hardcoded password


# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405

# Your stuff...
# ------------------------------------------------------------------------------

THIRD_PARTY_APPS = [
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "config.vcr_middleware.VCRMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "config.middleware.CacheHeaderMiddleware",
    "config.middleware.RobotsTagMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
    "config.middleware.FeedbackLinkMiddleware",
    "config.middleware.StructuredBreadcrumbsMiddleware",
    "waffle.middleware.WaffleMiddleware",
]

VCR_ENABLED = os.getenv("VCR_ENABLED", "true").lower() == "true"
VCR_MODE = os.getenv("VCR_MODE", "playback")
VCR_CASSETTE_DIR = str(ROOT_DIR / "vcr_cassettes")

if VCR_ENABLED:
    os.makedirs(VCR_CASSETTE_DIR, exist_ok=True)


# Only allow Storybook CORS in dev
DEBUG = env.bool("DJANGO_DEBUG", default=True)

if DEBUG:
    # Storybook iframe runs on port 6006 in dev
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:6006",
        "http://127.0.0.1:6006",
    ]
else:
    # Production Storybook served from same domain — no CORS
    CORS_ALLOWED_ORIGINS = []

STORYBOOK_SERVER = env(
    "STORYBOOK_SERVER",
    default="http://localhost:3000",
)
