
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/like/', views.toggle_like, name='toggle_like'),

    path('manage/', views.manage_games, name='manage_games'),
    path('manage/add/', views.add_game, name='add_game'),
    path('manage/edit/<int:game_id>/', views.edit_game, name='edit_game'),
    path('manage/delete/<int:game_id>/', views.delete_game, name='delete_game'),
]
