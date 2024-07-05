from django.contrib.auth import login, authenticate, get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignUpSerializer, PetInfoSerializer, LoginSerializer ,CheckUserIDSerializer
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

# 임시 토큰 생성 함수
def create_temp_access_token(user):
    from rest_framework_simplejwt.tokens import AccessToken
    from datetime import timedelta
    
    access = AccessToken.for_user(user)
    access.set_exp(lifetime=timedelta(minutes=5))  # 임시 토큰의 만료 시간을 5분으로 설정
    return str(access)

# 회원가입을 처리하는 API 뷰
@csrf_exempt  # CSRF 검증 비활성화
@swagger_auto_schema(
    method='post',
    operation_summary="회원가입",
    operation_description="회원가입을 처리합니다. 이메일, 사용자 ID, 이름, 생일, 비밀번호,전화번호를 입력받습니다.",
    request_body=SignUpSerializer,
    responses={
        201: '회원가입 성공',
        400: '잘못된 요청',
        500: '서버 오류'
    }
)
@api_view(['POST'])  # POST 요청만 허용
@permission_classes([AllowAny])  # 회원가입은 누구나 가능
def signup_view(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():  # 데이터가 유효할 때
            user = serializer.save()  # 사용자 생성
            login(request, user)  # 사용자 로그인
            print("User created and logged in:", user)  # 로그 추가
            
            # 임시 토큰 생성 펫 정보 입력 할 때 유효한 토큰 발급
            temp_access_token = create_temp_access_token(user)
            # 응답시에 유저 정보와 임시 토큰을 반환
            response_data = serializer.data
            response_data['phone'] = user.phone  # 전화번호 필드 추가
            
            return Response({
                'user': response_data,
                'temp_access_token': temp_access_token
            }, status=status.HTTP_201_CREATED)  # 201 Created 상태코드 반환

        print("Validation errors:", serializer.errors)  # 로그 추가
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 Bad Request 상태코드 반환


# 반려동물 정보 API 뷰
@swagger_auto_schema(
    method='post',
    operation_summary="반려동물 정보 입력",
    operation_description="로그인된 사용자의 반려동물 정보를 입력합니다.",
    request_body=PetInfoSerializer,
    responses={
        200: PetInfoSerializer,
        400: '잘못된 요청입니다.',
        401: '인증 실패입니다.',
        500: '서버 오류'
    }
)
@api_view(['POST'])
def pet_info_view(request):
    if request.method == 'POST':
        user = request.user
        serializer = PetInfoSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user.pet_name = validated_data.get('pet_name')
            user.pet_type = validated_data.get('pet_type')
            user.pet_photo = validated_data.get('pet_photo')
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인 API 뷰
@swagger_auto_schema(
    method='post',
    operation_summary="로그인",
    operation_description="사용자가 로그인합니다.",
    request_body=LoginSerializer,
    responses={
        200: openapi.Response('로그인 성공', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                'access_token': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )),
        400: '잘못된 요청입니다.',
        401: '인증 실패입니다.',
        500: '서버 오류'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=user_id, password=password)

            if user is not None: # 사용자 인증 성공
                login(request, user) # 사용자 로그인

                # 정식 JWT 토큰 생성
                refresh = RefreshToken.for_user(user)  # RefreshToken 객체 생성
                access_token = str(refresh.access_token)  # 액세스 토큰 추출
                refresh_token = str(refresh)  # 리프레시 토큰 추출

                # 응답에 액세스 토큰과 리프레시 토큰을 포함하여 반환

                return Response({
                    'refresh_token': refresh_token,
                    'access_token': access_token,
                }, status=status.HTTP_200_OK)

            print("Invalid credentials for user_id:", user_id)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        print("Login validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

@swagger_auto_schema(
    method='post',
    operation_summary="ID 중복 체크",
    operation_description="사용자가 입력한 ID의 중복 여부를 확인합니다.",
    request_body=CheckUserIDSerializer,
    responses={
        200: openapi.Response('사용 가능', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'available': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            }
        )),
        400: '잘못된 요청입니다.'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def check_user_id(request):
    serializer = CheckUserIDSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        if User.objects.filter(user_id=user_id).exists():
            return Response({'available': False}, status=status.HTTP_200_OK)
        else:
            return Response({'available': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)