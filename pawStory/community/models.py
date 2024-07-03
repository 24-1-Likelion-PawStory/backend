
# community/models.py

from django.db import models
from users.models import Member  # users 앱의 Member 모델을 가져옴

# 게시글 모델
class Post(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)  # Member 모델과 1:N 관계 설정
    title = models.CharField(max_length=50)  # 제목
    content = models.TextField()  # 내용
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)  # 좋아요 수

    def __str__(self):
        return self.title

# 댓글 모델
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Post 모델과 1:N 관계 설정
    user = models.ForeignKey(Member, on_delete=models.CASCADE)  # Member 모델과 1:N 관계 설정
    content = models.TextField()  # 내용
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

# 게시물-좋아요 다대다 풀기
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Post 모델과 1:N 관계 설정
    user = models.ForeignKey(Member, on_delete=models.CASCADE)  # Member 모델과 1:N 관계 설정
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}님이 {self.post}에 좋아요'  # 사용자가 게시글에 좋아요를 눌렀다는 의미로 문자열 반환

# 태그 모델
class Tag(models.Model):
    name = models.CharField(max_length=20)  # 태그 이름
    part = models.CharField(max_length=4, choices=[
        ('TOG', '같이해요'),
        ('QST', '궁금해요'),
        ('INF', '정보공유'),
        ('DAI', '일상공유')  # [로 잘못된 부분 수정]
    ])

    def __str__(self):
        return self.name

# 게시글-태그의 다대다 풀기
class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Post 모델과 1:N 관계 설정
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Tag 모델과 1:N 관계 설정

    def __str__(self):
        return f'{self.post}에 달린 {self.tag}'  # 게시글에 달린 태그를 문자열로 반환

