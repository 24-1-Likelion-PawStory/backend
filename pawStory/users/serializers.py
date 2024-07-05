# serializers.py
from rest_framework import serializers
from .models import Member

# 회원가입 시리얼라이저
class SignUpSerializer(serializers.ModelSerializer): #이때는 반려동물정보받지않음
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Member
        fields = ('id','user_id', 'email', 'name', 'user_bir', 'password','phone')
    
    # 유효성 검사를 통과한 데이터를 사용하여 새로운 사용자 인스턴스를 생성
    def create(self, validated_data):
        user = Member.objects.create(
            user_id=validated_data['user_id'],
            email=validated_data['email'],
            name=validated_data['name'],
            user_bir=validated_data['user_bir'],
            phone=validated_data.get('phone', '')  # 전화번호 필드 추가
            
        )
        user.set_password(validated_data['password']) # 비밀번호 해싱
        user.save()
        return user
    
# 반려동물 정보 시리얼라이저    
class PetInfoSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Member
        fields = ('pet_name', 'pet_type', 'pet_photo')  

# 로그인 시리얼라이저
class LoginSerializer(serializers.Serializer): 
    user_id = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        return super().validate(attrs)
    
# 사용자 ID 중복 확인 시리얼라이저
class CheckUserIDSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=20)