from django.contrib import admin
from .models import User, Developer, Genre, Game, Purchase, Review


admin.site.register(User)
admin.site.register(Developer)
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(Purchase)
admin.site.register(Review)