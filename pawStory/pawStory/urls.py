from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# 스웨거 설정하느라 추가
from django.urls import path, include, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="프로젝트 이름(예: likelion-project)",
        default_version='프로젝트 버전(예: 1.1.1)',
        description="해당 문서 설명(예: likelion-project API 문서)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="likelion@inha.edu"),
        license=openapi.License(name="backend"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('community/', include('community.urls')),
    path('diaries/', include('diaries.urls')),
    path('users/', include('users.urls')),
    # 스웨거
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 미디어 파일을 제공할 수 있도록 URL 패턴 추가
