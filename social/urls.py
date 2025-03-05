from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home # ✅ Import view home

urlpatterns = [
    # ✅ หน้าแรก
    path("", home, name="home"), #✅ redirect to home view

    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
