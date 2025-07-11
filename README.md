# Проект «YaMDb API»

### Описание

   Проект YaMDb собирает отзывы пользователей на произведения.  
   Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.<br/>    
   Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос),    
разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.<br/>    
   Добавлять произведения, категории и жанры может только администратор.<br/>    
   Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы  
и ставят произведению оценку в диапазоне от одного до десяти (целое число);  
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).<br/>  
   Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.<br/>    

### Стэк технологий
- проект написан на Python с использованием Django REST Framework
- библиотека Simple JWT - работа с JWT-токеном
- библиотека django-filter - фильтрация запросов
- база данных - SQLite
- система управления версиями - Git

### Используемые пакеты:
    * requests==2.26.0
    * Django==3.2
    * djangorestframework==3.12.4
    * PyJWT==2.1.0
    * pytest==6.2.4
    * pytest-django==4.4.0
    * pytest-pythonpath==0.7.3
    * djangorestframework-simplejwt==5.2.2
    * django-filter==22.1
    * python-dotenv==0.21.1

### Алгоритм регистрации пользователей
- Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами *email* и *username* на эндпоинт /api/v1/auth/signup/.
- **YaMDB** отправляет письмо с кодом подтверждения (*confirmation_code*) на адрес *email*.
- Пользователь отправляет POST-запрос с параметрами *username* и *confirmation_code* на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
- При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (*user*) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (*moderator*) — те же права, что и у А**утентифицированного пользователя** плюс право удалять любые отзывы и комментарии.
- **Администратор** (*admin*) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** — обладает правами администратора (*admin*)

### Ресурсы API YaMDb
- Ресурс AUTH: аутентификация.
- Ресурс USERS: пользователи.
- Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песня).
- Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Установка

1. Клонировать репозиторий:

   ```python
   git clone ...
   ```

2. Перейти в папку с проектом:

   ```python
   cd api_yamdb/
   ```

3. Установить виртуальное окружение для проекта:

   ```python
   python -m venv venv
   ```

4. Активировать виртуальное окружение для проекта:

   ```python
   # для OS Lunix и MacOS
   source venv/bin/activate
   # для OS Windows
   source venv/Scripts/activate
   ```

5. Установить зависимости:

   ```python
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Выполнить миграции на уровне проекта:

   ```python
   cd api_yamdb
   python manage.py migrate
   ```

7. Запустить проект:
   ```python
   python manage.py runserver
   ```

### Дополнительно

* **Загрузка тестовых данных**  
  В проекте есть management-команда для загрузки данных из CSV-файлов в базу данных.  
  Файлы должны находиться в директории `static/data/`.  
  Доступные CSV-файлы:
  - `users.csv` – пользователи
  - `category.csv` – категории
  - `genre.csv` – жанры
  - `titles.csv` – произведения
  - `review.csv` – отзывы
  - `comments.csv` – комментарии
  - `genre_title.csv` – связи жанров и произведений

  Для загрузки данных выполните команду:
   ```
   python manage.py load_data
   ```
* Каждый ресурс описан в документации проекта:
   ```
   http://127.0.0.1:8000/redoc/
   ```

* ПО для тестирования API:
   ```
   https://www.postman.com/
   ```

### Примеры запросов

* Пример POST-запроса<br/>   
    Регистрация нового пользователя и получение `confirmation_code`. Доступно без токена.  
    `POST http://127.0.0.1:8000/api/v1/auth/signup/`
    ```json
    {
        "email": "user@example.com",
        "username": "string"
    }
    ```
* Пример ответа:
    ```json
    {
        "email": "string",
        "username": "string"
    }
    ```
  В проекте настроен filebased способ отправки почты, confirmation_code будет находится в папке send_email базовой директории.
* Получение JWT-токена в обмен на `username` и `confirmation_code`. Доступно без токена.  
    `POST http://127.0.0.1:8000/api/v1/auth/token/`
    ```json
    {
        "username": "string",
        "confirmation_code": "string"
    }
    ```
* Пример ответа:
    ```json
    {
        "token": "string"
    }
    ```
  В дальнейшем token передаётся в Header: Bearer
* Создание отзыва к произведению. Необходим токен.  
    `POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/`
    ```json
    {
        "text": "string",
        "score": 1
    }
    ```
* Пример ответа:
    ```json
    {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
    }
    ```

### Авторы проекта
* Александр Давыдов
* Сергей Гусев
* Лев Азаретов