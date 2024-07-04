from rest_framework import generics
from users.models import Member
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Bearer Token 헤더 파라미터 정의
authorization_header = openapi.Parameter(
    'Authorization', 
    openapi.IN_HEADER, 
    description="Bearer [JWT token]", 
    type=openapi.TYPE_STRING, 
    required=True
)

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="프로필 조회",
        operation_description="특정 회원의 프로필을 조회합니다.",
        responses={
            200: ProfileSerializer,
            404: '해당 일기를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response
