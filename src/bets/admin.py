from django.contrib import admin
from bets.models import Bet
# Register your models here.
class BetAdmin(admin.ModelAdmin):
	list_display=('bet_id','teama','teamb','oddsa','oddsb')
	

admin.site.register(Bet,BetAdmin)