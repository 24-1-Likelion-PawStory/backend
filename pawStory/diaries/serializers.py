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
        fields = ['photo', 'content', 'is_public']  # member 필드 제외

    def create(self, validated_data):
        member = self.context['request'].user
        return Diary.objects.create(member=member, **validated_data)

class DiarySerializer(serializers.ModelSerializer):
    member = MemberDiarySerializer(read_only=True)
    comments = DiaryCommentSerializer(many=True, read_only=True, source='diary_comments')
    like_count = serializers.IntegerField(source='diary_likes.count', read_only=True)
    comment_count = serializers.IntegerField(source='diary_comments.count', read_only=True)

    class Meta:
        model = Diary
        fields = ['id', 'photo', 'content', 'created_at', 'is_public', 'member', 'comments', 'like_count', 'comment_count']

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
