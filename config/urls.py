from django.contrib import admin
from django.urls import path
from games.views import (
    home, game_detail,
    manage_games, add_game,
    edit_game, delete_game
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('game/<int:game_id>/', game_detail, name='game_detail'),
    path('manage/', manage_games, name='manage_games'),
    path('manage/add/', add_game, name='add_game'),
    path('manage/edit/<int:game_id>/', edit_game, name='edit_game'),
    path('manage/delete/<int:game_id>/', delete_game, name='delete_game'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)