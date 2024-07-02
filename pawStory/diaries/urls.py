from django.urls import path
from .views import *

urlpatterns = [
    path('diaries', DiaryListView.as_view(), name='diary-list'), # 일기 목록 조회
    path('diaries/<int:pk>', DiaryDetailView.as_view(), name='diary-detail'), # 일기 상세 조회, 수정, 삭제
    path('diaries', DiaryCreateView.as_view(), name='diary-create'), # 일기 작성
    path('diaries/<int:id>/like', DiaryLikeCreateView.as_view(), name='diary-like'), # 일기 좋아요
    path('diaries/<int:id>/like', DiaryLikeDeleteView.as_view(), name='diary-unlike'), #  일기 좋아요 취소
    path('diaries/<int:id>/comments', DiaryCommentCreateView.as_view(), name='diary-comment-create'), # 일기 댓글 작성
    path('diaries/<int:id>/comments', DiaryCommentListView.as_view(), name='diary-comment-list'), # 일기 댓글 조회
    path('diaries/<int:id>/comments/<int:comment_id>', DiaryCommentDeleteView.as_view(), name='diary-comment-delete'), # 일기 댓글 삭제
    path('follow', FollowCreateView.as_view(), name='follow-create'), # 팔로우
    path('unfollow', FollowDeleteView.as_view(), name='follow-delete'), # 언팔로우
]
