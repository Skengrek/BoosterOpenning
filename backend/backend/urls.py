from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from users.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # Cards API
    path("api/cards/", include("cards.urls")),
    # User API
    path("api/users/", include("users.urls")),
    # for admin side
    path("admin/", admin.site.urls),
    # JWT
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
