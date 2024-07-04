from rest_framework import serializers
from .models import Post, PostLike, PostComment, Tag
from users.models import Member

# 멤버 시리얼라이저
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'user_id', 'pet_photo']  # 멤버 모델에서 id, user_id, pet_photo 필드를 포함

# 태그 시리얼라이저
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'part']  # 태그 모델에서 name과 part 필드를 포함

# 댓글 시리얼라이저
class PostCommentSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)  # 댓글 작성자를 멤버 시리얼라이저로 포함

    class Meta:
        model = PostComment
        fields = ['id', 'content', 'user']  # 댓글 모델에서 id, content, user 필드를 포함

# 좋아요 시리얼라이저
class PostLikeSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)  # 좋아요 누른 사용자를 멤버 시리얼라이저로 포함

    class Meta:
        model = PostLike
        fields = ['id','user']  # 좋아요 모델에서 id와 user 필드를 포함

# 포스트 생성 시리얼라이저
class PostCreateSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(write_only=True)  # 태그를 문자열로 입력받고 쓰기 전용으로 설정

    class Meta:
        model = Post
        fields = ['title', 'content', 'tag']  # 포스트 모델에서 title, content, tag 필드를 포함

    def create(self, validated_data):
        tag_name = validated_data.pop('tag')  # 입력받은 태그 이름 추출
        tag_part = self.get_tag_part(tag_name)  # 태그 이름을 코드 값으로 변환
        user = self.context['request'].user  # 현재 요청을 보낸 사용자 가져오기
        tag, created = Tag.objects.get_or_create(name=tag_name, part=tag_part)  # 태그가 없으면 생성, 있으면 가져오기
        post = Post.objects.create(user=user, tag=tag, **validated_data)  # 새로운 포스트 생성 시 태그와 함께 저장
        return post

    def get_tag_part(self, tag_name):
        tag_mapping = {
            '같이해요': 'TOG',
            '궁금해요': 'QST',
            '정보공유': 'INF',
            '일상공유': 'DAI'
        }
        return tag_mapping.get(tag_name, 'OTH')  # 태그 이름을 코드로 변환, 기본값은 'OTH'

# 포스트 시리얼라이저
class PostSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)  # 작성자를 멤버 시리얼라이저로 포함, 읽기 전용
    comments = PostCommentSerializer(many=True, read_only=True, source='postcomment_set')  # 댓글을 포함
    like_count = serializers.IntegerField(source='postlike_set.count', read_only=True)  # 좋아요 수를 포함
    comment_count = serializers.IntegerField(source='postcomment_set.count', read_only=True)  # 댓글 수를 포함
    tag = TagSerializer(read_only=True)  # 태그를 태그 시리얼라이저로 포함

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user', 'comments', 'like_count', 'comment_count', 'tag']  # 포스트 모델에서 필요한 필드 포함

# 포스트리스트 시리얼라이저
class PostListSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)  # 태그를 태그 시리얼라이저로 포함

    class Meta:
        model = Post
        fields = ['id', 'title','tag']  # 포스트 모델에서 id, title, tag 필드를 포함