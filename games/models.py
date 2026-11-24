from django.db import models
from django.conf import settings


class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)


class Developer(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Game(models.Model):
    developer = models.ForeignKey(
        Developer,
        on_delete=models.CASCADE,
        db_index=True
    )
    genres = models.ManyToManyField(Genre)
    name = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    price = models.IntegerField(db_index=True)
    release_date = models.DateField(db_index=True)
    cover = models.ImageField(upload_to='game_covers/', blank=True, null=True)
    likes_count = models.PositiveIntegerField(default=0)

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

