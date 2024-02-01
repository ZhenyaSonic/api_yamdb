import csv
from django.db import transaction
from django.core.management.base import BaseCommand
from reviews.models import (Category,
                            Comment,
                            Genres,
                            GenreTitle,
                            Review,
                            Title,
                            CustomUser)

model_csv_equal = {
    'static/data/category.csv': Category,
    'static/data/genre.csv': Genres,
    'static/data/titles.csv': Title,
    'static/data/genre_title.csv': GenreTitle,
    'static/data/users.csv': CustomUser,
    'static/data/review.csv': Review,
    'static/data/comments.csv': Comment,
}


class Command(BaseCommand):
    info = 'Импорт csv файлов в таблицы базы'

    def _create_correct_row_fields(self, row):
        """Дополняет строку таблицы экземплярами модели."""
        try:
            if row.get('author'):
                row['author'] = CustomUser.objects.get(pk=row['author'])
            if row.get('review_id'):
                row['review'] = Review.objects.get(pk=row['review_id'])
            if row.get('title_id'):
                row['title'] = Title.objects.get(pk=row['title_id'])
            if row.get('category'):
                row['category'] = Category.objects.get(pk=row['category'])
            if row.get('genre'):
                row['genre'] = Genres.objects.get(pk=row['genre'])
        except Exception as error:
            print(f'Ошибка в строке {row.get("id")}.\n'
                  f'Текст - {error}')
        return row

    def handle(self, *args, **options):
        """Тело команды."""
        for path, model in model_csv_equal.items():
            print(f'Наполняем модель {model.__name__}')
            rows = 0
            successful = 0
            with open(path, encoding='utf-8', mode='r') as file:
                csv_read = csv.DictReader(file)
                with transaction.atomic():
                    for row in csv_read:
                        rows += 1
                        row = self._create_correct_row_fields(row)
                        try:
                            obj, created = model.objects.get_or_create(**row)
                            if created:
                                successful += 1
                        except Exception as error:
                            print(f'Ошибка в строке {row.get("id")}.\n'
                                  f'Текст - {error}')
            print(f'Наполнение модели {model.__name__} завершено. '
                  f'Строк: {rows}. Успешно: {successful}.')
