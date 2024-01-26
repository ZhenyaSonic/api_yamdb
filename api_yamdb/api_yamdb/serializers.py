from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from reviews.models import Title, Review, Comment, CustomUser
from .constants import MAX_LENGTH_NAME, MAX_LENGTH_EMAIL
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
import random
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'category', 'description', 'rating')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'bio', 'role')


class CustomRoleSerializer(CustomUserSerializer):

    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=MAX_LENGTH_NAME,
        required=True,
    )

    email = serializers.EmailField(
        required=True,
        max_length=MAX_LENGTH_EMAIL
    )

    class Meta:
        model = CustomUser
        lookup_field = 'username'
        fields = ('email', 'username')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('username', 'email',),
                message=('Такой пользователь уже зарегистрирован.')
            )
        ]

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        confirmation_code = random.randint(100000, 999999)

        if not CustomUser.objects.filter(
                username=username,
                email=email).exists():
            user = CustomUser.objects.create(
                email=email,
                username=username,
                confirmation_code=confirmation_code)
            send_mail(
                subject=f'Подтверждение регистрации {username}',
                message=f'Ваш код подтверждения: {confirmation_code}',
                from_email=f'{settings.EMAIL_SENDER}',
                recipient_list=[validated_data['email']],
                fail_silently=False)

            return user


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True
    )

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(CustomUser, username=username)
        if user is None:
            raise serializers.ValidationError(
                'Такого пользоателя не сущестует')
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError(
                'Введен неправильный код подтверждения')

        access = AccessToken.for_user(user)

        return {'token': str(access)}

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
