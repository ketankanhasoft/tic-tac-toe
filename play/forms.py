from django import forms
import random
from django.core.exceptions import ValidationError
from .models import Game

def validate_player_type(player_type):
    try:
        return player_type is not None
    except Exception as e:
        raise ValidationError("Unknown player type: " + player_type)

class NewGameForm(forms.Form):
    player1 = forms.CharField(max_length=64, required=True,
                              validators=[validate_player_type])
    player2 = forms.CharField(max_length=64, required=True,
                              validators=[validate_player_type])

    def create(self):
        "Creates a game."
        players = [self.cleaned_data['player1'], self.cleaned_data['player2']]
        random.shuffle(players)
        return Game.objects.create(player_x=players[0],
                                   player_o=players[1])


class PlayForm(forms.Form):
    index = forms.IntegerField(min_value=0, max_value=8)
