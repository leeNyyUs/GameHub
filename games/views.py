from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count

from .forms import GameForm
from .models import Game, Developer, Genre, Like


def home(request):
    games = Game.objects.annotate(
        likes_count=Count('like')
    )
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

    elif sort == 'popular':
        games = games.order_by('-likes_count', '-id')

    else:
        games = games.order_by('id')

    games = games.distinct()

    paginator = Paginator(games, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'games/home.html', {
        'games': page_obj,
        'page_obj': page_obj,
        'developers': Developer.objects.all(),
        'genres': Genre.objects.all(),
    })


def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    likes_count = Like.objects.filter(game=game).count()

    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(
            game=game,
            user=request.user
        ).exists()

    return render(request, 'games/game_detail.html', {
        'game': game,
        'likes_count': likes_count,
        'user_liked': user_liked,
    })


admin_required = user_passes_test(lambda user: user.is_staff)


@admin_required
def manage_games(request):
    games = Game.objects.select_related('developer').prefetch_related('genres')
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


def toggle_like(request, game_id):
    if not request.user.is_authenticated:
        return redirect('login')

    game = get_object_or_404(Game, id=game_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        game=game
    )

    if not created:
        like.delete()

    return redirect('game_detail', game_id=game.id)
