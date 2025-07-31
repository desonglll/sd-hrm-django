from tkinter.font import names

from django.conf.urls.static import static
from django.urls import include, path
from home import urls as home_urls
from user.views import CurrentUserView
from . import settings
from .routers import sd_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from home import views as home_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("navbar/", home_views.navbar_view, name="navbar"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('user/me/', CurrentUserView.as_view()),
    path("", include(sd_router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("home/", include(home_urls.urlpatterns)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
