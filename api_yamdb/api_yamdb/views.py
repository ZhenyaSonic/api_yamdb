# import jwt
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from reviews.models import CustomUser
from .permissions import AdminOnlyPermission
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django.conf import settings

# from django.core.mail import send_mail
# from django.conf import settings
# from datetime import datetime, timedelta
# import random
# import string

from .serializers import (
    TitleSerializer, ReviewSerializer, CommentSerializer,
    CustomUserSerializer, UserProfileUpdateSerializer,
    SignUpSerializer, TokenSerializer
)
from reviews.models import Title, Review, Comment
from django.http import HttpResponseBadRequest

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# class UserSignupView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = UserSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()

#             # Генерация JWT-токена
#             token = self.generate_jwt_token(user)

#             # Отправка письма с кодом подтверждения
#             confirmation_code = self.generate_confirmation_code()
#             send_confirmation_email(user.email, confirmation_code)

#             response_data = {
#                 'detail': 'Confirmation email sent successfully.',
#                 'token': token
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        if not request.data:
            return HttpResponseBadRequest(
                'No data provided. Please provide the necessary data in your PATCH request.'
            )

        serializer = UserProfileUpdateSerializer(
            instance=request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AdminOnlyPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [SearchFilter]
    search_fields = ('username',)

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