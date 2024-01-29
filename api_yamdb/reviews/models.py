from django.db import models
from django.contrib.auth.models import AbstractUser


from api.constants import (
    MAX_LENGTH_BIO,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME,
    MAX_LENGTH_ROLE,
    USER_ROLES,
    ADMIN, USER, MODERATOR
)


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

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

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
    name = models.CharField(max_length=100)
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

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    # Добавьте другие поля, необходимые для модели произведения


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    user_id = models.IntegerField()  # Временное обходное решение
    text = models.CharField(
        max_length=300
    )
    rating = models.IntegerField()  # Можно назвать score скорее всего

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text
    # Добавьте другие поля, необходимые для модели отзывов


class Genres(models.Model):
    """Модель жанры, многое к многому"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug
