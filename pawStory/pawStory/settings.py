import os
import json
from pathlib import Path
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# secrets.json 파일에서 시크릿 키 값 로드하기
secret_file = BASE_DIR / 'secrets.json'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # 프로젝트 루트의 static 디렉토리
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f'Set the {setting} environment variable')

# 시크릿키와 서명키 가져오기
SECRET_KEY = get_secret('SECRET_KEY')
SIGNING_KEY = get_secret('SIGNING_KEY')

# 미디어 파일을 저장할 디렉터리 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEBUG = False

ALLOWED_HOSTS = [ '3.37.90.199', 
    'pawstory.p-e.kr',
    '127.0.0.1',
    'localhost',
    'pawstory-s3.s3-website.ap-northeast-2.amazonaws.com',
]

INSTALLED_APPS = [
    #my apps
    'community',
    'diaries',
    'users',
    'accounts',
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
    'drf_yasg',

]

AUTH_USER_MODEL = 'users.Member' # 사용자 모델을 커스텀 유저 모델로 변경

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

CORS_ALLOW_METHODS = [  # 허용할 옵션
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [  # 허용할 헤더
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://3.37.90.199",
    "https://pawstory.p-e.kr",
    "http://pawstory-s3.s3-website.ap-northeast-2.amazonaws.com",
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
    'SIGNING_KEY': SIGNING_KEY,
		# JWT에서 가장 중요한 인증키입니다! 
		# 이 키가 알려지게 되면 JWT의 인증체계가 다 털릴 수 있으니 노출되지 않게 조심해야합니다!
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
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


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
