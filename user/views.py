from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from sd_hrm.permissions import IsAdminOrReadOnly
from user.models import User
from sd_hrm.pagination import StandardResultsSetPagination
from user.serializers import UserSerializer, ContentTypeSerializer, PermissionSerializer, GroupSerializer
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['username', 'id']  # 允许排序的字段
    ordering = ['username']  # 默认排序字段
    filterset_fields = [
        'username',
        'phone',
        'id_number',
        'is_active',
        'is_staff',
        'is_superuser'
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        query_params = self.request.query_params.dict()
        filters = {}

        for key, value in query_params.items():
            if key in ['page', 'page_size']:
                continue
            if value == '':
                continue

            if '__' in key:
                field, lookup = key.split('__', 1)
                if field in self.filterset_fields:
                    filters[f"{field}__{lookup}"] = value
            elif key in self.filterset_fields:
                filters[key] = value

        if filters:
            queryset = queryset.filter(**filters)
        ordering = self.request.query_params.get('ordering')
        if ordering is None:
            # 如果是列表，取第一个字段
            ordering = self.ordering[0] if isinstance(self.ordering, (list, tuple)) else self.ordering

        if ordering:
            if ordering.lstrip('-') not in self.ordering_fields:
                raise ValidationError(f"Invalid ordering field: {ordering}")
            queryset = queryset.order_by(ordering)

        return queryset


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.data)
        return Response(UserSerializer(request.user).data)


class ResetPasswordAPIView(APIView):
    """
    POST /api/reset-password/
    {
        "username": "example_user",
        "new_password": "new_secure_password"
    }
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        username = request.data.get('id')
        new_password = request.data.get('new_password')

        if not username or not new_password:
            return Response({"detail": "用户名和新密码不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"detail": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

        user.password = make_password(new_password)
        user.save()

        return Response({"detail": "密码重置成功"}, status=status.HTTP_200_OK)
