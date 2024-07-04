from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Diary, DiaryLike, DiaryComment, Follow, Member
from .serializers import DiaryCreateSerializer, DiarySerializer, DiaryListSerializer, DiaryLikeSerializer, DiaryCommentSerializer, FollowSerializer
from rest_framework.exceptions import ValidationError

class DiaryCreateView(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiaryCreateSerializer
    permission_classes = [IsAuthenticated]

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

class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        response = super().update(request, *args, **kwargs)
        return response

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        response = super().partial_update(request, *args, **kwargs)
        return response

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
