from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Permission, Group
from api.constants import (
    MAX_LENGTH_BIO,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME,
    MAX_LENGTH_ROLE,
    USER_ROLES,
)


user = get_user_model()


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Уникальный login пользователя',
        max_length=MAX_LENGTH_NAME,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_LENGTH_NAME,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=MAX_LENGTH_NAME,
        blank=True
    )
    email = models.EmailField(
        verbose_name='Email пользователя',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=MAX_LENGTH_ROLE,
        choices=USER_ROLES,
        default='user',
        blank=True,
        help_text='Выберете роль пользователя'
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        max_length=MAX_LENGTH_BIO,
        blank=True
    )
    confirmation_code = models.CharField(
        'Поле с кодом подтверждения',
        max_length=6
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        related_name='custom_users'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Права пользователя',
        blank=True,
        related_name='custom_users'
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='uq_username_email'
            )
        ]

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        'имя категории',
        max_length=200
    )
    slug = models.SlugField(
        'слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField('название произведения', max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'описание',
        max_length=255,
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        'рейтинг',
        default=None,
        null=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    author = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    text = models.TextField(
        'текст отзыва',
        null=False
    )
    score = models.IntegerField(
        'оценка произведения',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.TextField(
        'текст комментария',
        null=False
    )
    author = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
