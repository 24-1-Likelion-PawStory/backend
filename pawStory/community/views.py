from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError 
from .models import Post, PostLike, PostComment, Tag
from .serializers import PostCreateSerializer, PostSerializer, PostListSerializer, PostLikeSerializer, PostCommentSerializer

# 게시물 생성 뷰
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()  
    serializer_class = PostCreateSerializer  # 게시물 생성 시리얼라이저 사용
    permission_classes = [IsAuthenticated]  

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data, context={'request': request})  # 요청 데이터를 기반으로 시리얼라이저 생성
        serializer.is_valid(raise_exception=True) 
        post = self.perform_create(serializer)  # 게시물 생성
        headers = self.get_success_headers(serializer.data)  # 응답 헤더 설정
        post_serializer = PostSerializer(post, context={'request': request})  # 생성된 게시물 데이터를 포함한 시리얼라이저 생성
        return Response(post_serializer.data, status=status.HTTP_201_CREATED, headers=headers)  #

    def perform_create(self, serializer): 
        return serializer.save()

# 게시물 목록 조회 뷰
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')  # 생성일 기준으로 내림차순 정렬된 모든 게시물 쿼리셋
    serializer_class = PostListSerializer  # 게시물 목록 시리얼라이저 사용
    permission_classes = [IsAuthenticated]  

# 게시물 상세 조회, 수정, 삭제 뷰
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()  
    serializer_class = PostSerializer  
    permission_classes = [IsAuthenticated]  

# 좋아요 생성 뷰
class PostLikeCreateView(generics.CreateAPIView):
    queryset = PostLike.objects.all()  
    serializer_class = PostLikeSerializer  
    permission_classes = [IsAuthenticated]  #

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.kwargs['post_id'])  # 게시물 ID를 기반으로 게시물 가져오기
            serializer.save(user=self.request.user, post=post)  # 좋아요 저장
        except Post.DoesNotExist:
            raise ValidationError("좋아요를 누를 게시물을 찾을 수 없습니다.")  # 게시물이 없을 경우 예외 처리

# 좋아요 삭제 뷰
class PostLikeDeleteView(generics.DestroyAPIView):
    queryset = PostLike.objects.all() 
    serializer_class = PostLikeSerializer  
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        try:
            return PostLike.objects.get(post_id=self.kwargs['post_id'], user=self.request.user)  # 게시물 ID와 사용자 정보를 기반으로 좋아요 객체 가져오기
        except PostLike.DoesNotExist:
            raise ValidationError("좋아요를 찾을 수 없습니다")  # 좋아요가 없을 경우 예외 처리

# 댓글 생성 뷰
class PostCommentCreateView(generics.CreateAPIView):
    queryset = PostComment.objects.all()  
    serializer_class = PostCommentSerializer  
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_id'])  # 게시물 ID를 기반으로 게시물 가져오기
        serializer.save(user=self.request.user, post=post)  # 댓글 저장

# 댓글 목록 조회 뷰
class PostCommentListView(generics.ListAPIView):
    serializer_class = PostCommentSerializer  # 댓글 시리얼라이저 사용
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        post_id = self.kwargs['post_id']  # URL에서 게시물 ID 가져오기
        return PostComment.objects.filter(post_id=post_id)  # 해당 게시물에 달린 댓글들 가져오기

# 댓글 삭제 뷰
class PostCommentDeleteView(generics.DestroyAPIView):
    queryset = PostComment.objects.all() 
    serializer_class = PostCommentSerializer  
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        return PostComment.objects.get(pk=self.kwargs['comment_id'], post_id=self.kwargs['post_id'])  # 댓글 ID와 게시물 ID를 기반으로 댓글 객체 가져오기

# 태그별 게시물 목록 조회 뷰
class PostByTagListView(generics.ListAPIView):
    serializer_class = PostSerializer 
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        tag_part = self.kwargs.get('tag_part')  # URL에서 태그 부분 코드 가져오기
        return Post.objects.filter(tag__part=tag_part)  # 해당 태그 부분에 맞는 게시물들 가져오기
