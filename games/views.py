from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import GameForm
from django.shortcuts import render, get_object_or_404
from .models import Game, Developer, Genre


def home(request):
    games = Game.objects.all()

    search = request.GET.get('search', '')
    developer = request.GET.get('developer', '')
    genre = request.GET.get('genre', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '')

    if search:
        games = games.filter(name__icontains=search)

    if developer:
        games = games.filter(developer_id=developer)

    if genre:
        games = games.filter(genres__id=genre)

    if min_price:
        games = games.filter(price__gte=min_price)

    if max_price:
        games = games.filter(price__lte=max_price)

    if sort == 'price_asc':
        games = games.order_by('price')

    elif sort == 'price_desc':
        games = games.order_by('-price')

    elif sort == 'name':
        games = games.order_by('name')

    elif sort == 'date':
        games = games.order_by('-release_date')

    games = games.distinct()

    return render(request, 'games/home.html', {
        'games': games,
        'developers': Developer.objects.all(),
        'genres': Genre.objects.all(),
    })


def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'games/game_detail.html', {'game': game})


admin_required = user_passes_test(lambda user: user.is_staff)


@admin_required
def manage_games(request):
    games = Game.objects.all()

    return render(request, 'games/manage.html', {
        'games': games
    })


@admin_required
def add_game(request):
    form = GameForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        game = form.save()
        print("ИГРА СОХРАНЕНА:", game.name)
        return redirect('manage_games')
    else:
        print("ОШИБКИ ФОРМЫ:", form.errors)

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
