from django import forms
from .models import Game


class GameForm(forms.ModelForm):
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