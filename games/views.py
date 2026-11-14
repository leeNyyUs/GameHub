from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import GameForm
from django.shortcuts import render, get_object_or_404
from .models import Game


def home(request):
    games = Game.objects.all()

    return render(request, 'games/home.html', {
        'games': games
    })

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    return render(request, 'games/game_detail.html', {
        'game': game
    })

# Проверка доступа к админ-панели
admin_required = user_passes_test(lambda user: user.is_staff)


# Главная страница админки
@admin_required
def manage_games(request):
    games = Game.objects.all()

    return render(request, 'games/manage.html', {
        'games': games
    })


# Добавление игры
@admin_required
def add_game(request):
    form = GameForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('manage_games')

    return render(request, 'games/game_form.html', {
        'form': form,
        'title': 'Добавить игру'
    })


@admin_required
def add_game(request):
    form = GameForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('manage_games')

    return render(request, 'games/game_form.html', {
        'form': form,
        'title': 'Добавить игру'
    })


@admin_required
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    form = GameForm(
        request.POST or None,
        request.FILES or None,
        instance=game
    )

    if form.is_valid():
        form.save()
        return redirect('manage_games')

    return render(request, 'games/game_form.html', {
        'form': form,
        'title': 'Изменить игру'
    })

@admin_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        game.delete()

    return redirect('manage_games')
