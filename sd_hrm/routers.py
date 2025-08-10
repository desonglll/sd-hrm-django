from rest_framework import routers

from user.views import UserViewSet, PermissionViewSet, ContentTypeViewSet, GroupViewSet, ResetPasswordAPIView

sd_router = routers.DefaultRouter()
sd_router.register(r"users", UserViewSet)
sd_router.register(r"permissions", PermissionViewSet)
sd_router.register(r"contenttypes", ContentTypeViewSet)
sd_router.register(r"groups", GroupViewSet)
