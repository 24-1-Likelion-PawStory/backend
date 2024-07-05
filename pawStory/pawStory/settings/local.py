from .base import *

ALLOWED_HOSTS = []
DEBUG = True

# 로컬 데이터베이스 설정 (예: SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}