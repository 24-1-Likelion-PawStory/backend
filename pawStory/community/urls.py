from django.urls import path
from .views import *

urlpatterns = [
    path('posts', PostListView.as_view(), name='post-list'),  # 게시물 목록 조회
    path('posts/create', PostCreateView.as_view(), name='post-create'),  # 게시물 생성
    path('posts/<int:pk>', PostDetailView.as_view(), name='post-detail'),  # 게시물 상세 조회, 수정, 삭제
    path('posts/<int:post_id>/like', PostLikeCreateView.as_view(), name='post-like'),  # 게시물 좋아요 생성
    path('posts/<int:post_id>/unlike', PostLikeDeleteView.as_view(), name='post-unlike'),  # 게시물 좋아요 삭제
    path('posts/<int:post_id>/comments', PostCommentListView.as_view(), name='post-comment-list'),  # 게시물 댓글 목록 조회
    path('posts/<int:post_id>/comments/create', PostCommentCreateView.as_view(), name='post-comment-create'),  # 게시물 댓글 생성
    path('posts/<int:post_id>/comments/<int:comment_id>', PostCommentDeleteView.as_view(), name='post-comment-delete'),  # 게시물 댓글 삭제
    path('posts/tag/<str:tag_part>', PostByTagListView.as_view(), name='post-by-tag'),  # 태그별 게시물 조회
]
