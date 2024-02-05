import random
import datetime as dt
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.conf import settings

from reviews.models import User, Category, Genres, Title, Review, Comment
from .constants import MAX_LENGTH_NAME, MAX_LENGTH_EMAIL


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'role')


class RoleSerializer(UserSerializer):

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

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username "me" is not allowed.'
            )
        return value

    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('email', 'username')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email',),
                message=('Такой пользователь уже зарегистрирован.')
            )
        ]

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        confirmation_code = random.randint(100000, 999999)

        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            defaults={'confirmation_code': confirmation_code}
        )

        if not created:
            raise serializers.ValidationError(
                {'detail': 'Такой пользователь уже зарегистрирован.'}
            )

        send_mail(
            subject=f'Подтверждение регистрации {username}',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=f'{settings.EMAIL_SENDER}',
            recipient_list=[validated_data['email']],
            fail_silently=False
        )

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

        user = get_object_or_404(User, username=username)
        if user is None:
            raise serializers.ValidationError(
                'Такого пользоателя не сущестует')
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError(
                'Введен неправильный код подтверждения')

        access = AccessToken.for_user(user)

        return {'token': access}

    def to_representation(self, instance):
        return {'token': str(instance['token'])}

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    """Основной метод записи информации."""

    category = serializers.SlugRelatedField(
        slug_field='slug', many=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genres.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год')
        return value


class TitlesViewSerializer(serializers.ModelSerializer):
    """Основной метод получения информации."""

    category = CategorySerializer(many=False, required=True)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    def validate(self, attrs):
        request = self.context.get('request')
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    'Вы не можете создать больше одного отзыва на произведение'
                )
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
