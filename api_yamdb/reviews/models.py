from django.db import models
from django.contrib.auth.models import AbstractUser


from api_yamdb.constants import (
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
