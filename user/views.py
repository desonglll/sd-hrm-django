from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from sd_hrm.permissions import IsAdminOrReadOnly
from user.models import User
from sd_hrm.pagination import StandardResultsSetPagination
from user.serializers import UserSerializer
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]

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

        return queryset


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.data)
        return Response(UserSerializer(request.user).data)
