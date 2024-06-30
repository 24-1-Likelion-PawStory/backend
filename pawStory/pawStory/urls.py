from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('community/', include('community.urls')),
    path('diaries/', include('diaries.urls')),
    path('users/', include('users.urls')),
]
