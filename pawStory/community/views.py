# community/views.py
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated

class PostListCreateView(generics.ListCreateAPIView):  # ListCreateAPIView 사용
    queryset = Post.objects.all()  # 모든 Post 객체를 쿼리셋으로 설정
    serializer_class = PostSerializer  # PostSerializer를 사용하여 시리얼라이즈
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 현재 로그인한 사용자를 user 필드에 저장

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):  # 제네릭 뷰 사용, 상세 조회, 수정, 삭제
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    #변경사항뜨게하는용 ㅜ주석
