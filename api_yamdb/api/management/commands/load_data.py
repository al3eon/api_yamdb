import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')


class Command(BaseCommand):
    help = 'Загружает данные из CSV-файлов в базу данных'

    def handle(self, *args, **kwargs):
        self.load_users()
        self.load_categories()
        self.load_genres()
        self.load_titles()
        self.load_reviews()
        self.load_comments()
        self.load_genre_title()

    def load_csv(self, filename):
        path = os.path.join(DATA_DIR, filename)
        with open(path, encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def load_users(self):
        for row in self.load_csv('users.csv'):
            User.objects.get_or_create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )

    def load_categories(self):
        for row in self.load_csv('category.csv'):
            Category.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )

    def load_genres(self):
        for row in self.load_csv('genre.csv'):
            Genre.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )

    def load_titles(self):
        for row in self.load_csv('titles.csv'):
            Title.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )

    def load_reviews(self):
        for row in self.load_csv('review.csv'):
            Review.objects.get_or_create(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )

    def load_comments(self):
        for row in self.load_csv('comments.csv'):
            Comment.objects.get_or_create(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )

    def load_genre_title(self):
        for row in self.load_csv('genre_title.csv'):
            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])
            title.genre.add(genre)
