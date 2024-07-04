from django.contrib import admin
from .models import Member
from community.models import *

admin.site.register(Member)
admin.site.register(Post)
admin.site.register(PostComment)  # PostComment 모델 등록
admin.site.register(PostLike)