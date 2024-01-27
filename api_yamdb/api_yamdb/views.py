from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404

from reviews.models import CustomUser
from .permissions import AdminOnlyPermission
from .serializers import (
    CustomUserSerializer,
    SignUpSerializer, TokenSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AdminOnlyPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [SearchFilter]
    search_fields = ('username',)

    def perform_create(self, serializer):
        # Если разрешение проверено, создаем пользователя
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(
            CustomUser,
            username=self.kwargs[self.lookup_field])
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Signup(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        if user:
            return Response(request.data, status=status.HTTP_200_OK)

        response_data = {
            'email': user.email,
            'username': user.username,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class Token(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
