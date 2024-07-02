from rest_framework import serializers
from .models import *
from users.models import Member

class MemberDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'user_id', 'profile_image']  # 필요 시 추가 필드

class DiaryCommentSerializer(serializers.ModelSerializer):
    member = MemberDiarySerializer(read_only=True)
    
    class Meta:
        model = DiaryComment
        fields = ['id', 'content', 'created_at', 'member']

class DiaryLikeSerializer(serializers.ModelSerializer):
    member = MemberDiarySerializer(read_only=True)
    
    class Meta:
        model = DiaryLike
        fields = ['id', 'member']

class DiarySerializer(serializers.ModelSerializer):
    member = MemberDiarySerializer(read_only=True)
    likes = DiaryLikeSerializer(many=True, read_only=True, source='diary_likes')
    comments = DiaryCommentSerializer(many=True, read_only=True, source='diary_comments')
    like_count = serializers.IntegerField(source='diary_likes.count', read_only=True)
    comment_count = serializers.IntegerField(source='diary_comments.count', read_only=True)

    class Meta:
        model = Diary
        fields = ['id', 'photo', 'content', 'created_at', 'is_public', 'member', 'likes', 'comments', 'like_count', 'comment_count']

class DiaryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'photo']

class FollowSerializer(serializers.ModelSerializer):
    follower = MemberDiarySerializer(read_only=True)
    following = MemberDiarySerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']
