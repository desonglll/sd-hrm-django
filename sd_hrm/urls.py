from tkinter.font import names

from django.conf.urls.static import static
from django.urls import include, path
from home import urls as home_urls
from user.views import CurrentUserView, ResetPasswordAPIView
from . import settings
from .routers import sd_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from home import views as home_views

urlpatterns = [
    path("api/", include(sd_router.urls)),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("home/", include(home_urls.urlpatterns)),
    path("api/reset_password/", ResetPasswordAPIView.as_view(), name='reset-password'),
    path("api/user/me/", CurrentUserView.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
