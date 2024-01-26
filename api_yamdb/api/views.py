import jwt
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import random
import string

from .serializers import (
    TitleSerializer, ReviewSerializer, CommentSerializer,
    CustomUserSerializer, UserProfileUpdateSerializer
)
from reviews.models import Title, Review, Comment


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


class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Генерация JWT-токена
            token = self.generate_jwt_token(user)

            # Отправка письма с кодом подтверждения
            confirmation_code = self.generate_confirmation_code()
            self.send_confirmation_email(user.email, confirmation_code)

            response_data = {
                'detail': 'Confirmation email sent successfully.',
                'token': token
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_jwt_token(self, user):
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1),
            # Устанавливаем срок действия токена
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    def generate_confirmation_code(self):
        # Генерация кода подтверждения
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )

    def send_confirmation_email(self, email, confirmation_code):
        # Реализуйте отправку письма с кодом подтверждения
        subject = 'Код подтверждения'
        message = f'Ваш код подтверждения: {confirmation_code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [email])


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = UserProfileUpdateSerializer(
            instance=request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
