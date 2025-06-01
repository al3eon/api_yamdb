from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from users.models import User
from api.serializers import (
    UserSerializer, UserEditSerializer,
    SignupSerializer, TokenSerializer
)
from api.permissions import IsAdmin


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(username__icontains=search)
        return queryset

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Метод PUT не разрешен. Используйте PATCH.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserEditSerializer
    )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)
