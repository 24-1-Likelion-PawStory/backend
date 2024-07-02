from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Diary, DiaryLike, DiaryComment, Follow
from .serializers import DiarySerializer, DiaryListSerializer, FollowSerializer, DiaryCommentSerializer
from django.shortcuts import get_object_or_404

def api_response(data, message, status_code):
    response = {
        "message": message,
        "data": data
    }
    return Response(response, status=status_code)

class DiaryListView(generics.ListAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiaryListSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(serializer.data, "일기 목록 조회 성공", status.HTTP_200_OK)

class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return api_response(data=response.data, message="일기 조회 성공", status_code=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        response = super().update(request, partial=partial, *args, **kwargs)
        return api_response(data=response.data, message="일기 수정 성공", status_code=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        response = super().partial_update(request, partial=partial, *args, **kwargs)
        return api_response(data=response.data, message="일기 부분 수정 성공", status_code=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(None, "일기 삭제 성공", status_code=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        # 일기와 관련된 좋아요와 댓글 모두 삭제
        DiaryLike.objects.filter(diary=instance).delete()
        DiaryComment.objects.filter(diary=instance).delete()
        instance.delete()

class DiaryCreateView(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(data=response.data, message="일기 작성 성공", status_code=status.HTTP_201_CREATED)

class DiaryLikeCreateView(generics.CreateAPIView):
    queryset = DiaryLike.objects.all()
    serializer_class = DiaryLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        diary = get_object_or_404(Diary, id=self.kwargs['id'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(member=self.request.user, diary=diary)
        response = super().create(request, *args, **kwargs)
        return api_response(data=response.data, message="좋아요 성공", status_code=status.HTTP_201_CREATED)

class DiaryLikeDeleteView(generics.DestroyAPIView):
    queryset = DiaryLike.objects.all()
    serializer_class = DiaryLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(DiaryLike, member=self.request.user, diary__id=self.kwargs['id'])

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return api_response(None, "좋아요 취소 성공", status_code=status.HTTP_204_NO_CONTENT)

class DiaryCommentCreateView(generics.CreateAPIView):
    queryset = DiaryComment.objects.all()
    serializer_class = DiaryCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        diary = get_object_or_404(Diary, id=self.kwargs['id'])
        serializer.save(member=self.request.user, diary=diary)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(serializer.data, "댓글 작성 성공", status.HTTP_201_CREATED)

class DiaryCommentListView(generics.ListAPIView):
    serializer_class = DiaryCommentSerializer

    def get_queryset(self):
        return DiaryComment.objects.filter(diary__id=self.kwargs['id'])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return api_response(serializer.data, "댓글 목록 조회 성공", status.HTTP_200_OK)

class DiaryCommentDeleteView(generics.DestroyAPIView):
    queryset = DiaryComment.objects.all()
    serializer_class = DiaryCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(DiaryComment, id=self.kwargs['comment_id'], member=self.request.user)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return api_response(None, "댓글 삭제 성공", status_code=status.HTTP_204_NO_CONTENT)

class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        following_id = self.request.data.get('following')
        following = get_object_or_404(Member, id=following_id)
        serializer.save(follower=self.request.user, following=following)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(serializer.data, "팔로우 성공", status.HTTP_201_CREATED)

class FollowDeleteView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        following_id = self.request.data.get('following')
        return get_object_or_404(Follow, follower=self.request.user, following__id=following_id)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return api_response(None, "언팔로우 성공", status_code=status.HTTP_204_NO_CONTENT)
