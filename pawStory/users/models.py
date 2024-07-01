from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_id, name, pet_name, pet_type, user_bir, password=None, **extra_fields): # 일반 계정 생성 메서드
        if not email:
            raise ValueError('The Email field must be set')
        if not user_id:
            raise ValueError('The User ID field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        if not pet_name:
            raise ValueError('The Pet Name field must be set')
        if not pet_type:
            raise ValueError('The Pet Type field must be set')
        if not user_bir:
            raise ValueError('The User Birthdate field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            user_id=user_id,
            name=name,
            pet_name=pet_name,
            pet_type=pet_type,
            user_bir=user_bir,
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
            pet_name='SuperPet',  # 기본값 설정
            pet_type='DOG',       # 기본값 설정
            user_bir='2000-01-01',# 기본값 설정
            password=password,
            **extra_fields
        )

class Member(AbstractBaseUser, PermissionsMixin):
    class PetType(models.TextChoices):
        DOG = 'DOG', '개'
        CAT = 'CAT', '고양이'
        BIRD = 'BIRD', '새'
        FISH = 'FISH', '물고기'

    email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    pet_name = models.CharField(max_length=50)
    pet_type = models.CharField(
        max_length=4,
        choices=PetType.choices,
        default=PetType.DOG
    )
    user_bir = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
