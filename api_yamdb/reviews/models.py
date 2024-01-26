from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


user = get_user_model()


# class User(models.Model):
#     username = models.CharField('пользовательский ник', max_length=100)
#     email = models.EmailField(
#         'эмейл',
#         max_length=254,
#         unique=True,
#         blank=False,
#         null=False
#     )
#     first_name = models.CharField(
#         'имя',
#         max_length=150,
#         blank=True
#     )
#     last_name = models.CharField(
#         'фамилия',
#         max_length=150,
#         blank=True
#     )

#     class Meta:
#         ordering = ('id',)
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'

#     def __str__(self):
#         return self.username
#     # Добавьте другие поля, необходимые для модели пользователя


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
        return f'{self.name}'


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
    # Добавьте другие поля, необходимые для модели произведения


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
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    title = models.IntegerField()
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
