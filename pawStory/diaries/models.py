from django.db import models
from users.models import Member
from django.db.models import UniqueConstraint

# Create your models here.
class Diary(models.Model):
    PUBLIC = 'public'
    FOLLOWERS_ONLY = 'followers'
    PRIVATE = 'private'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (FOLLOWERS_ONLY, 'Followers only'),
        (PRIVATE, 'Private'),
    ]

    id = models.AutoField(primary_key=True) # 일기 키
    photo = models.ImageField(upload_to='diary_photos/') # 사진
    content = models.CharField(max_length=100) # 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일자
    is_public = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC) # 공개여부
    like_count = models.IntegerField(default=0) # 좋아요 수
    member = models.ForeignKey(Member, verbose_name="일기 작성자", on_delete=models.CASCADE, related_name="diary") # 회원정보 키

    def __str__(self):
        return self.content

class DiaryLike(models.Model):
    id = models.AutoField(primary_key=True) # 좋아요 키
    member = models.ForeignKey(Member, verbose_name="좋아요한 사람", on_delete=models.CASCADE, related_name="diary_likes") # 회원정보 키
    diary = models.ForeignKey(Diary, verbose_name="좋아요한 일기", on_delete=models.CASCADE, related_name="diary_likes") # 일기 키

    class Meta:
        constraints = [
                UniqueConstraint(fields=['member', 'diary'], name='unique_like')
            ]

    def __str__(self):
        return f"{self.member.user_id} likes {self.diary.content[:20]}"

class DiaryComment(models.Model):
    id = models.AutoField(primary_key=True) # 댓글 키
    content = models.CharField(max_length=100) # 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일자
    member = models.ForeignKey(Member, verbose_name="댓글 작성자", on_delete=models.CASCADE, related_name="diary_comments") # 회원정보 키
    diary = models.ForeignKey(Diary, verbose_name="일기", on_delete=models.CASCADE, related_name="diary_comments") # 일기 키

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.diary.comment_count = F('comment_count') + 1
            self.diary.save(update_fields=['comment_count'])
        super(DiaryComment, self).save(*args, **kwargs)

class Follow(models.Model):
    id = models.AutoField(primary_key=True) # 팔로우 키
    follower = models.ForeignKey(Member, verbose_name="팔로워", on_delete=models.CASCADE, related_name="following") # 팔로워 키 -> 역참조할 때는 그 사람 입장에서 이 모델이 자기가 팔로우한 사람들에 대한 것.
    following = models.ForeignKey(Member, verbose_name="팔로잉", on_delete=models.CASCADE, related_name="follower") # 팔로잉 키 -> 역참조할 때는 그 사람 입장에서 이 모델이 자기 팔로워에 대한 것

    class Meta:
        constraints = [
            UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]

    def __str__(self):
        return self.content
