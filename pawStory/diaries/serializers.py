from rest_framework import serializers
from .models import Diary, DiaryLike, DiaryComment, Follow
from users.models import Member

class MemberDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'user_id', 'pet_photo']

class DiaryCommentSerializer(serializers.ModelSerializer):
    member = MemberDiarySerializer(read_only=True)
    
    class Meta:
        model = DiaryComment
        fields = ['id', 'content', 'member']

class DiaryLikeSerializer(serializers.ModelSerializer):
    member = MemberDiarySerializer(read_only=True)
    
    class Meta:
        model = DiaryLike
        fields = ['id', 'member']

class DiaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'photo', 'content', 'is_public']

    def create(self, validated_data):
        member = self.context['request'].user
        diary = Diary.objects.create(member=member, **validated_data)
        return diary

class DiarySerializer(serializers.ModelSerializer):
    member = MemberDiarySerializer(read_only=True)
    likes = DiaryLikeSerializer(many=True, read_only=True, source='diary_likes')
    comments = DiaryCommentSerializer(many=True, read_only=True, source='diary_comments')
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Diary
        fields = ['id', 'photo', 'content', 'created_at', 'is_public', 'member', 'likes', 'comments', 'like_count', 'comment_count']

    def get_like_count(self, obj):
        return obj.diary_likes.count()

    def get_comment_count(self, obj):
        return obj.diary_comments.count()

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