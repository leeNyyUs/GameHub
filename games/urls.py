from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/like/', views.toggle_like, name='toggle_like'),
]