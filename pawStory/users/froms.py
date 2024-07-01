# forms.py
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import Member
import re # 정규표현식 사용을 위한 모듈

class SignUpForm(UserCreationForm): # 회원가입 폼
    class Meta:
        model = Member
        fields = ('user_id', 'email', 'name', 'pet_name', 'pet_type', 'user_bir', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email') # 이메일 필드 값 가져오기
        if Member.objects.filter(email=email).exists(): # 이메일 중복 검사
            raise forms.ValidationError("이 이메일은 이미 사용 중입니다.") # 중복 시 에러 발생
        return email # 중복이 없을 시 값 반환

    def clean_user_id(self): # 사용자 ID 필드 유효성 검사
        user_id = self.cleaned_data.get('user_id')
        if Member.objects.filter(user_id=user_id).exists(): # 사용자 ID 중복 검사
            raise forms.ValidationError("이 사용자 ID는 이미 사용 중입니다.") # 중복 시 에러 발생
        return user_id # 중복이 없을 시 값 반환
    
    def clean_password1(self): # 비밀번호 필드 유효성 검사
        password1 = self.cleaned_data.get("password1")

        # 비밀번호 복잡성 검사
        if len(password1) < 12:
            raise forms.ValidationError("비밀번호는 12자 이상이어야 합니다.")
        if not re.search(r'[A-Za-z]', password1):
            raise forms.ValidationError("비밀번호에는 영문자가 포함되어야 합니다.")
        if not re.search(r'\d', password1):
            raise forms.ValidationError("비밀번호에는 숫자가 포함되어야 합니다.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError("비밀번호에는 특수문자가 포함되어야 합니다.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return password2
    
    def clean_user_bir(self):
        user_bir = self.cleaned_data.get('user_bir')
        if not user_bir:
            raise forms.ValidationError("생년월일을 입력해 주세요.")
        return user_bir 
    
    def clean_pet_type(self):
        pet_type = self.cleaned_data.get('pet_type')
        if not pet_type:
            raise forms.ValidationError("반려동물 종류를 선택해 주세요.")
        return pet_type
    
    