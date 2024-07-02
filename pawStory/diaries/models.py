from django.db import models
from pawStory.users.models import Member

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

    def __str__(self):
        return self.content

    # def clean(self): # clean 메서드를 통해 유효성 검사
    #     # 일기 작성자가 스스로 좋아요를 누르지 않도록 검사
    #     if self.member_id == self.diary_id.member_id:
    #         raise ValidationError("작성자는 자신의 일기에 좋아요를 누를 수 없습니다.")

    # def save(self, *args, **kwargs):
    #     # 저장하기 전에 clean 메서드 호출
    #     self.clean()
    #     super(DiaryLike, self).save(*args, **kwargs)

class DiaryComment(models.Model):
    id = models.AutoField(primary_key=True) # 댓글 키
    content = models.CharField(max_length=100) # 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일자
    member = models.ForeignKey(Member, verbose_name="댓글 작성자", on_delete=models.CASCADE, related_name="diary_comments") # 회원정보 키
    diary = models.ForeignKey(Diary, verbose_name="일기", on_delete=models.CASCADE, related_name="diary_comments") # 일기 키

    def __str__(self):
        return self.content

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
