from django.contrib.auth import login, authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated  # *수정*
from rest_framework_simplejwt.tokens import RefreshToken  # *수정*
from .serializers import SignUpSerializer, PetInfoSerializer, LoginSerializer

User = get_user_model()  # 커스텀 유저 모델 가져오기

# 회원가입을 처리하는 API 뷰
@csrf_exempt  #CSRF 검증 비활성화
@api_view(['POST'])  # POST 요청만 허용
@permission_classes([AllowAny])  #회원가입은 누구나 가능
def signup_view(request):
    print("Received data:", request.data)  # 로그 추가
    if request.method == 'POST':  # POST 요청일 때
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():  # 데이터가 유효할 때
            user = serializer.save()  # 사용자 생성
            login(request, user)  # 사용자 로그인
            print("User created and logged in:", user)  # 로그 추가
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 201 Created 상태코드 반환
        print("Validation errors:", serializer.errors)  # 로그 추가
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 Bad Request 상태코드 반환

# 반려동물 정보를 처리하는 API 뷰
@csrf_exempt  # CSRF 검증 비활성화
@api_view(['POST'])  # POST 요청만 허용
# @permission_classes([IsAuthenticated])  #반려동물 정보 입력은 JWT인증된 사용자만 가능
def pet_info_view(request):
    print("Received pet info data:", request.data)  # 로그 추가
    if request.method == 'POST':
        user = request.user  # 요청한 사용자를 가져옴 (로그인된 사용자) 이래야 회원가입에서 이어서 반려동물 입력
        serializer = PetInfoSerializer(data=request.data)
        # if serializer.is_valid():
        # 유효한 경우 사용자의 반려동물 정보를 업데이트
        user.pet_name = serializer.validated_data.get('pet_name')
        user.pet_type = serializer.validated_data.get('pet_type')
        user.pet_photo = serializer.validated_data.get('pet_photo')
        user.save()
        print("Pet info updated for user:", user)  # 로그 추가
        return Response(serializer.data, status=status.HTTP_200_OK)  # 성공 응답 반환
        # print("Pet info validation errors:", serializer.errors)  # 로그 추가
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 오류 응답 반환

# 로그인 처리 API 뷰
@csrf_exempt
@api_view(['POST']) # POST 요청만 허용
@permission_classes([AllowAny]) # 로그인은 누구나 가능
def login_view(request):
    print("Received login data:", request.data)
    if request.method == 'POST': 
        serializer = LoginSerializer(data=request.data) 
        if serializer.is_valid(): 
            user_id = serializer.validated_data.get('user_id') 
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=user_id, password=password)
            if user is not None: # 사용자 인증 성공
                login(request, user) # 사용자 로그인
                refresh = RefreshToken.for_user(user)  # JWT 토큰 생성
                return Response({
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            print("Invalid credentials for user_id:", user_id)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        print("Login validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
