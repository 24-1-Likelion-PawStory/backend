# Django REST framework 설정으로, API의 권한 및 인증 방식을 설정합니다.
from datetime import timedelta
from pathlib import Path
from decouple import config
import os  # 추가

BASE_DIR = Path(__file__).resolve().parent.parent

from django.core.exceptions import ImproperlyConfigured
import json

secret_file = BASE_DIR / 'secrets.json'

BASE_DIR = Path(__file__).resolve().parent.parent # 프로젝트 디렉토리의 경로를 설정합니다.

MEDIA_URL = '/media/'  # 미디어 파일을 제공할 URL을 설정합니다.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 미디어 파일이 저장될 경로를 설정합니다.


with open(secret_file) as file:
    secrets = json.loads(file.read())

def get_secret(setting,secrets_dict = secrets):
    try:
        return secrets_dict[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret('SECRET_KEY') 
# 위의 과정들을 통해 json 파일의 secrets.json 파일을 읽어 SECRET_KEY 값을 할당해줍니다
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    #my apps
    'community',
    'diaries',
    'users',
    #basic apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #external apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

]

AUTH_USER_MODEL = 'users.Member' # 사용자 모델을 커스텀 유저 모델로 변경

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', 
    # 이 미들웨어는 장고가 풀스택으로 사용될 때 csrf 공격을 막기 위해 csrf token을 발급하기 위한 미들웨어입니다!
    # 백엔드 개발시에 csrf 관련 미들웨어가 있으면 아마 잦은 에러를 해결하셔야 할거에요! 
    # 이 미들웨어는 주석 또는 삭제 처리 해주시면 됩니다!
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

 

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 인증된 요청인지 확인
        #'rest_framework.permissions.AllowAny',  # 누구나 접근 가능
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT를 통한 인증방식 사용
    ),
}

SIMPLE_JWT = {
    'SIGNING_KEY': config('SIGNING_KEY'), 
		# JWT에서 가장 중요한 인증키입니다! 
		# 이 키가 알려지게 되면 JWT의 인증체계가 다 털릴 수 있으니 노출되지 않게 조심해야합니다!
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
		# access token의 유효시간을 설정합니다.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
		# refresh token의 유효시간을 설정합니다.
    'ROTATE_REFRESH_TOKENS': False,
		# True로 설정하면 리프레시 토큰이 사용될 때마다 새로운 리프레시 토큰이 발급됩니다.
    'BLACKLIST_AFTER_ROTATION': True,
		# 리프레시 토큰 회전 후, 이전의 리프레시 토큰이 블랙리스트에 추가될지 여부를 나타내는 부울 값입니다. 
		# True로 설정하면 리프레시 토큰이 회전되면서, 이전의 리프레시 토큰은 블랙리스트에 추가되어 더 이상 사용할 수 없게 됩니다.
}
# JWT 설정으로, JSON Web Token의 특정 속성을 설정합니다.
ROOT_URLCONF = 'pawStory.urls'

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

WSGI_APPLICATION = 'pawStory.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ko-kr' # 언어를 한국어로 변경해줍니다

TIME_ZONE = 'Asia/Seoul' # 시간대를 서울로 변경해줍니다

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

