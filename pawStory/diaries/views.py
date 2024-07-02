from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Diary, DiaryLike, DiaryComment, Follow
from .serializers import DiaryCreateSerializer, DiarySerializer, DiaryListSerializer, DiaryLikeSerializer, DiaryCommentSerializer, FollowSerializer

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
        serializer.save()

class DiaryListView(generics.ListAPIView):
    queryset = Diary.objects.all().order_by('-created_at')
    serializer_class = DiaryListSerializer
    permission_classes = [IsAuthenticated]

class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

class DiaryLikeCreateView(generics.CreateAPIView):
    queryset = DiaryLike.objects.all()
    serializer_class = DiaryLikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        diary = Diary.objects.get(pk=self.kwargs['id'])
        serializer.save(member=self.request.user, diary=diary)

class DiaryLikeDeleteView(generics.DestroyAPIView):
    queryset = DiaryLike.objects.all()
    serializer_class = DiaryLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return DiaryLike.objects.get(diary_id=self.kwargs['id'], member=self.request.user)

class DiaryCommentCreateView(generics.CreateAPIView):
    queryset = DiaryComment.objects.all()
    serializer_class = DiaryCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        diary = Diary.objects.get(pk=self.kwargs['id'])
        serializer.save(member=self.request.user, diary=diary)

class DiaryCommentListView(generics.ListAPIView):
    serializer_class = DiaryCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        diary_id = self.kwargs['id']
        return DiaryComment.objects.filter(diary_id=diary_id)

class DiaryCommentDeleteView(generics.DestroyAPIView):
    queryset = DiaryComment.objects.all()
    serializer_class = DiaryCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return DiaryComment.objects.get(pk=self.kwargs['comment_id'], diary_id=self.kwargs['id'])

class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        follower = self.request.user
        following = Member.objects.get(pk=self.request.data['following'])
        serializer.save(follower=follower, following=following)

class FollowDeleteView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        follower = self.request.user
        following = Member.objects.get(pk=self.request.data['following'])
        return Follow.objects.get(follower=follower, following=following)