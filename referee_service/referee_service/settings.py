"""
Django settings for referee_service project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')3x0-_ldo3(olga-v&rkan_7!@57wc4^hjt0*ccd@w^svseh-m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'referee_service',
    'api',
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

ROOT_URLCONF = 'referee_service.urls'

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

WSGI_APPLICATION = 'referee_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ping_pong',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

########## REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    
}
########## END REST FRAMEWORK CONFIGURATION

PLAYER_DATA_FILE_NAME= "players_data.json"
GAME_WINNING_POINTS = 5
# GET_PLAYERS_URL = "http://127.0.0.1:8001/player/api/v1/players/"
# GET_PLAYER_MOVES_URL = "http://127.0.0.1:8001/player/api/v1/moves/"
# PLAYER_SHUTDOWN_URL = "http://127.0.0.1:8001/player/api/v1/shut-down/"

PLAYER_STATUS = {"Registered": "Registered", "Selected":"Selected", "Playing":"Playing", "Winner":"Winner",
                "Looser":"Looser", "Shutdown":"Shutdown"}

PLAYER_ROLE = {"N/A":"Not Defined","Offensive":"Offensive", "Defensive":"Defensive"}

CHAMPIONSHIP_STATUS = {"Started":"Started","Ended":"Ended"}

GAME_STATUS = {"Drawn":"Drawn", "Started":"Started", "InProgress":"InProgress","Done":"Done"}

REGISTERED_NOTIFICATION = "Players have registered with championship"
DRAW_GAMES_INSTRUCTION = "Lets draw Initial Games"
DRAW_GAMES_NOTIFICATION = "{0} Games Drawn"
PLAYER_LOGIN_INSTRUCTION = "Game is {0} vs {1} Please Login as one of them."
TOSS_NOTIFICATION = "{0} will be {1} and {2} will be {3}"
TOSS_INSTRUCTION = "Offensive player start with moves"

START_MATCH_NOTIFICATION = "Start Game with offensive player {0} select random number from 1 to 10."
START_MATCH_INSTRUCTION = "Defensive player {0} create a defense array of random numbers (from 1 to 10) of length {1}"

SHUTDOWN_NOTIFICATION = "Defeated Players were shutdown "
NEXT_ROUND_INSTRUCTION = "Draw Games for next Round"

