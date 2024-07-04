from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Diary, DiaryLike, DiaryComment, Follow, Member
from .serializers import DiaryCreateSerializer, DiarySerializer, DiaryListSerializer, DiaryLikeSerializer, DiaryCommentSerializer, FollowSerializer
from rest_framework.exceptions import ValidationError
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

class DiaryCreateView(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiaryCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="일기 작성",
        operation_description="새로운 일기를 작성합니다. 필요한 파라미터는 사진, 내용, 공개방식입니다.",
        request_body=DiaryCreateSerializer,
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            201: DiaryCreateSerializer,
            400: '잘못된 요청입니다.',
            500: '서버 오류입니다.'
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

class DiaryListView(generics.ListAPIView):
    queryset = Diary.objects.all().order_by('-created_at')
    serializer_class = DiaryListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="일기 목록 조회",
        operation_description="모든 일기의 목록을 조회합니다.",
         manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            200: DiaryListSerializer(many=True),
            400: '잘못된 요청입니다.',
            500: '서버 오류입니다.'
        }
    )
    def get(self, request, *args, **kwargs):  # get 메서드 추가
        response = super().list(request, *args, **kwargs)
        return response

class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="일기 상세 조회",
        operation_description="특정 일기의 상세 정보를 조회합니다.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            200: DiarySerializer,
            404: '해당 일기를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response

    @swagger_auto_schema(
        operation_summary="일기 수정",
        operation_description="특정 일기의 내용을 수정합니다.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        request_body=DiarySerializer,
        responses={
            200: DiarySerializer,
            400: '잘못된 요청입니다.',
            404: '해당 일기를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        response = super().update(request, *args, **kwargs)
        return response

    @swagger_auto_schema(
        operation_summary="일기 삭제",
        operation_description="특정 일기를 삭제합니다.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            204: '삭제됨',
            404: '해당 일기를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        # 일기와 관련된 좋아요와 댓글 모두 삭제
        DiaryLike.objects.filter(diary=instance).delete()
        DiaryComment.objects.filter(diary=instance).delete()
        instance.delete()

class DiaryLikeCreateView(generics.CreateAPIView):
    queryset = DiaryLike.objects.all()
    serializer_class = DiaryLikeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="일기 좋아요 생성",
        operation_description="특정 일기에 좋아요를 추가합니다.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            201: DiaryLikeSerializer,
            404: '해당 일기를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def post(self, request, *args, **kwargs):
        diary = get_object_or_404(Diary, id=self.kwargs['id'])
        if DiaryLike.objects.filter(member=self.request.user, diary=diary).exists():
            raise ValidationError('You have already liked this diary.')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(member=self.request.user, diary=diary)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DiaryLikeDeleteView(generics.DestroyAPIView):
    queryset = DiaryLike.objects.all()
    serializer_class = DiaryLikeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="일기 좋아요 삭제",
        operation_description="특정 일기에서 좋아요를 삭제합니다.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            204: '삭제됨',
            404: '좋아요를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def get_object(self):
        return DiaryLike.objects.get(diary_id=self.kwargs['id'], member=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class DiaryCommentCreateView(generics.CreateAPIView):
    queryset = DiaryComment.objects.all()
    serializer_class = DiaryCommentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="일기 댓글 생성",
        operation_description="특정 일기에 댓글을 추가합니다.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        request_body=DiaryCommentSerializer,
        responses={
            201: DiaryCommentSerializer,
            404: '해당 일기를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def perform_create(self, serializer):
        diary = Diary.objects.get(pk=self.kwargs['id'])
        serializer.save(member=self.request.user, diary=diary)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DiaryCommentListView(generics.ListAPIView):
    serializer_class = DiaryCommentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="일기 댓글 목록 조회",
        operation_description="특정 일기에 달린 모든 댓글을 조회합니다.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            200: DiaryCommentSerializer(many=True),
            404: '댓글을 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def get_queryset(self):
        diary_id = self.kwargs['id']
        return DiaryComment.objects.filter(diary_id=diary_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DiaryCommentDeleteView(generics.DestroyAPIView):
    queryset = DiaryComment.objects.all()
    serializer_class = DiaryCommentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="일기 댓글 삭제",
        operation_description="특정 일기에서 댓글을 삭제합니다.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            204: '삭제됨',
            404: '해당 댓글을 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def get_object(self):
        return DiaryComment.objects.get(pk=self.kwargs['comment_id'], diary_id=self.kwargs['id'])

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="팔로우",
        operation_description="특정 사용자를 팔로우합니다. 팔로우할 사용자를 파라미터로 입력해주세요.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        request_body=FollowSerializer,
        responses={
            201: FollowSerializer,
            404: '해당 사용자를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def perform_create(self, serializer):
        follower = self.request.user
        following = Member.objects.get(pk=self.request.data['following'])
        if follower == following:
            raise ValidationError('You cannot follow yourself.')
        if Follow.objects.filter(follower=follower, following=following).exists():
            raise ValidationError('You are already following this user.')
        serializer.save(follower=follower, following=following)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FollowDeleteView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="팔로우 취소",
        operation_description="특정 사용자 팔로우를 취소합니다. 취소할 사용자를 파라미터로 넣어주세요.",
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer [JWT token]",
            type=openapi.TYPE_STRING,
            required=True
        )],
        responses={
            204: '삭제됨',
            404: '해당 사용자를 찾을 수 없습니다.',
            500: '서버 오류입니다.'
        }
    )
    def get_object(self):
        follower = self.request.user
        following = Member.objects.get(pk=self.request.data['following'])
        return Follow.objects.get(follower=follower, following=following)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
