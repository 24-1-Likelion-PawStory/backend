from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
import os

def user_directory_path(instance, filename):

    return 'user_{0}/{1}'.format(instance.user_id, filename)

class CustomUserManager(BaseUserManager): 
    def create_user(self, email, user_id, name, user_bir, password=None, **extra_fields): # 일반 계정 생성 메서드
        if not email:
            raise ValueError('이메일은 반드시 입력해야합니다.')
        if not user_id:
            raise ValueError('ID는 반드시 입력해야합니다')
        if not name:
            raise ValueError('이름은 반드시 입력해야 합니다.')
        if not user_bir:
            raise ValueError('생일은 반드시 입력해야 합니다.')
        if not password:
            raise ValueError('패스워드는 반드시 입력해야합니다.')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            user_id=user_id,
            name=name,
            user_bir=user_bir,
            pet_name='Default Pet Name', # 기본값 설정을 통해 회원가입만
            pet_type='DOG', # 기본값 설정 회원가입만처리
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_id, name, password=None, **extra_fields): # 슈퍼계정 생성 메서드
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user( # create_user 메서드 재사용
            email=email,
            user_id=user_id,
            name=name,
            user_bir='2000-01-01', # 기본값 설정
            password=password,
            **extra_fields
        )

class Member(AbstractBaseUser, PermissionsMixin): # 사용자 모델 정의
    class PetType(models.TextChoices):
        DOG = 'DOG', '개'
        CAT = 'CAT', '고양이'
        BIRD = 'BIRD', '새'
        FISH = 'FISH', '물고기'
    # 사용자 모델 필드 정의
    email = models.EmailField(unique=True) 
    user_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    pet_name = models.CharField(max_length=50, null=True, blank=True)
    pet_type = models.CharField(
        max_length=4,
        choices=PetType.choices,
        default=PetType.DOG,
        null=True,
        blank=True
    )
    pet_photo = models.ImageField(upload_to='pet_photos/', null=True, blank=True)
    user_bir = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id' # 유저 아이디를 로그인에 사용
    REQUIRED_FIELDS = ['email', 'name'] # 필수 입력 필드

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
