from bets.models import Bet
from django.forms import ModelForm
from django import forms


class BetForm(forms.ModelForm):
	CHOICES = (
		(11,'Pilka Nozna'),
		(12,'Żużel'),
		(13,'Koszykowka'),
		(14,'Hokej'),
		(15,'Boks'),
		(16,'Piłka Ręczna'),
	)
	category = forms.ChoiceField(choices=CHOICES)
	class Meta:
		model = Bet
		fields = ('category','teama','teamb','oddsa','oddsx','oddsb','game_date')