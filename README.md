# api_yamdb
Групповой проект api_yamdb
Технологии:
Python 3.10
Django 3.2
Djangorestframework 3.12.4

Запуск проекта в dev-режиме
Клонировать репозиторий и перейти в него в командной строке:

    git clone <ссылка с git-hub>
Cоздать виртуальное окружение:

windows
    python -m venv venv

linux
    python3 -m venv venv

Активируйте виртуальное окружение
windows
    source venv/Scripts/activate

linux
    source venv/bin/activate

Установите зависимости из файла requirements.txt

    pip install -r requirements.txt
В папке с файлом manage.py выполните команду:

windows
    python manage.py runserver

linux
    python3 manage.py runserver

Документация к проекту
Документация для API после установки доступна по адресу

    http://127.0.0.1/redoc/
Примеры запросов
GET-Response: http://127.0.0.1:8000/api/v1/titles/1/
Request:

{
    "id": 1,
    "name": "Побег из Шоушенка",
    "year": 1994,
    "description": null,
    "genre": [
        {
            "name": "Драма",
            "slug": "drama"
        }
    ],
    "category": {
        "name": "Фильм",
        "slug": "movie"
    },
    "rating": 10
}
GET-Response: http://127.0.0.1:8000/api/v1/titles/1/reviews/1/
Request:

{
    "id": 1,
    "author": "bingobongo",
    "title": 1,
    "text": 
        "Ставлю десять звёзд!\n...Эти голоса были чище и светлее тех,
        о которых мечтали в этом сером, убогом месте. Как будто две птички 
        влетели и своими голосами развеяли стены наших клеток, и на короткий
        миг каждый человек в Шоушенке почувствовал себя свободным.",
    "score": 10,
    "pub_date": "2024-01-31T18:06:02.054698Z"
}
Авторы
Студенты курса "Python-разработчик" от Яндекс-Практикума:

Евгений Братанов:

модели, view и эндпойнты для:
произведений,
категорий,
жанров;
импорт данных из csv файлов

Борисов Максим:

система регистрации и аутентификации,
права доступа,
работа с токеном,
система подтверждения через e-mail

Клищенко Павел:

модели, view и эндпойнты для:
отзывов,
комментариев,
рейтинга произведений