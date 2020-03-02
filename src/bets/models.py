from django.db import models
from account.models import User
from decimal import Decimal
import datetime 
from datetime import date

# Create your models here.
class Bet(models.Model):
	bet_id=models.AutoField(primary_key=True)
	category=models.CharField(max_length=30)
	teama=models.CharField(max_length=50)
	teamb=models.CharField(max_length=50)
	oddsa=models.DecimalField(max_digits=8, decimal_places=2,default=1)
	oddsx=models.DecimalField(max_digits=8, decimal_places=2,default=1)
	oddsb=models.DecimalField(max_digits=8, decimal_places=2,default=1)
	game_date=models.DateField(verbose_name="game_date")
	finalscore=models.CharField(max_length=50,default="0",blank=True, null=True)

	



	def set_teama(self,team):
		if isinstance(team,str):
				self.teama=team
				self.save()
				return True
		else:
			return False

	def set_teamb(self,team):
		if isinstance(team,str):
				self.teamb=team
				self.save()
				return True
		else:
			return False

	def set_oddsa(self,odds):
		if isinstance(odds,Decimal) or isinstance(odds,float) or isinstance(odds,int):
			self.oddsa=odds
			self.save()
			return True
		else:
			return False

	def set_oddsb(self,money):
		if isinstance(odds,Decimal) or isinstance(odds,float) or isinstance(odds,int):
			self.oddsb=odds
			self.save()
			return True
		else:
			return False

	def is_in_future(self):
		if self.game_date<datetime.date.today():
			return False
		else:
			return True

	def __str__(self):
		return self.teama

class PlacedBet(models.Model):
	placed_bet_id=models.AutoField(primary_key=True)
	bet_id=models.ManyToManyField(Bet)
	pick=models.CharField(max_length=50)
	is_won=models.BooleanField(blank=True, null=True, default=None)

	def get_odds(self):
		bet=self.bet_id.all()
		if self.pick=="1":
			return bet[0].oddsa
		else:
			return bet[0].oddsb
	
	
class Coupon(models.Model):	
	coupon_id=models.AutoField(primary_key=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	stake=models.DecimalField(max_digits=8, decimal_places=2,default=1)
	is_placed=models.BooleanField(default=False)
	status=models.BooleanField(blank=True, null=True, default=None)
	placedbets=models.ManyToManyField(PlacedBet)
		
	def is_coupon_won(self):
		placedbets=self.placedbets.all()
		for tempplacedbet in placedbets:
			if tempplacedbet.is_won is None:
				return False
			elif tempplacedbet.is_won is False:
				self.status=False
				self.save()
				return False
		
		currentuser=self.user
		currentuser.customer.money=currentuser.customer.won_money(self.stake*self.total_odds())
		currentuser.customer.save()
		self.status=True
		self.save()
		return True
	
	def total_odds(self):
		total=1
		placedbets=self.placedbets.all()
		for tempplacedbet in placedbets:
			total=total*tempplacedbet.get_odds()
		return total

	def is_stake_minimal(self,stake):
		
		if stake>=1.0:
			return True
		else: 
			return False
		
	


	