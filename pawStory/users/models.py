from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager): # CustomUserManager 클래스를 생성합니다
    def create_user(self, email, user_id, name, pet_name, pet_type, user_bir, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
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

    def create_superuser(self, email, user_id, name, pet_name, pet_type, user_bir, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, user_id, name, pet_name, pet_type, user_bir, password, **extra_fields)

class Member(AbstractBaseUser, PermissionsMixin): # Member 클래스를 생성합니다
    class PetType(models.TextChoices): # PetType 클래스를 생성합니다
        DOG = 'DOG', '개'
        CAT = 'CAT', '고양이'
        BIRD = 'BIRD', '새'
        FISH = 'FISH', '물고기'

    email = models.EmailField(unique=True) # email 필드
    user_id = models.CharField(max_length=20, unique=True) # 중복불가
    name = models.CharField(max_length=50) # 이름 필드, 중복 가능
    pet_name = models.CharField(max_length=50) # 반려동물 이름 필드
    pet_type = models.CharField( # 반려동물 종류 필드
        max_length=4,
        choices=PetType.choices,
        default=PetType.DOG
    )
    user_bir = models.DateField() # 사용자 생년월일 필드
    created_at = models.DateTimeField(auto_now_add=True) # 생성일자 필드
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager() # CustomUserManager 클래스를 사용합니다

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'name', 'pet_name', 'pet_type', 'user_bir']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name