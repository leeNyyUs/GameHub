from django import forms
from .models import Game, Developer, Genre

class GameForm(forms.ModelForm):
    developer = forms.ModelChoiceField(
        queryset=Developer.objects.all(),
        empty_label="Выберите разработчика"
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple,
        required=True
    )

    release_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        )
    )

    class Meta:
        model = Game
        fields = [
            'name',
            'description',
            'developer',
            'genres',
            'price',
            'release_date',
            'cover'
        ]