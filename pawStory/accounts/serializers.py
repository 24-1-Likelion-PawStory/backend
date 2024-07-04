from rest_framework import serializers
from users.models import Member
from diaries.models import Diary, Follow

class ProfileSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ['id', 'pet_photo', 'user_id', 'post_count', 'follower_count', 'following_count']

    def get_post_count(self, obj):
        return Diary.objects.filter(member=obj).count()

    def get_follower_count(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()
