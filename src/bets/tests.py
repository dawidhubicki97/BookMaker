from django.test import TestCase
from bets.models import Bet,Coupon,PlacedBet
from account.models import User
from django.test.client import RequestFactory
from bets.views import show_bets_view, add_bet_view, show_bets_to_admin, enter_score, show_coupons_view
from django.urls import reverse,resolve
from bets.forms import BetForm
import datetime 
# Create your tests here.

class BetsTestClass(TestCase):
	def setUp(self):
		bet=Bet(teama="barcelona",teamb="real",oddsa=2.00,oddsx=3.20,oddsb=2.50,game_date="2020-02-21",category="11")
		bet.save()
		bettwo=Bet(teama="polska",teamb="anglia",oddsa=1.50,oddsb=2.50,game_date="2020-02-21",category="11")
		bettwo.save()			
		user=User(username="testowy",email="costam@gmail.com")
		user.set_password("haslo123")
		user.is_admin=False
		user.is_active=True
		user.is_customer=True
		user.save()
		user.customer.birth_date=datetime.date(1997,10,1)
		user.customer.money=500.0
		user.customer.save()		
		placedbet=PlacedBet(pick="1")
		placedbet.save()
		placedbet=PlacedBet.objects.get(pk=1)
		placedbet.bet_id.add(bet)
		placedbet.save()
		placedbettwo=PlacedBet(pick="1")
		placedbettwo.save()
		placedbettwo.bet_id.add(bettwo)
		placedbettwo.save()
		coupon=Coupon(user=user,stake=20,is_placed=True,status=None)
		coupon.save()	
		coupon.placedbets.add(placedbet) 
		coupon.placedbets.add(placedbettwo) 
		coupon.save()

	
	def test_totalodd(self):
		coupon=Coupon.objects.get(pk=1)
		self.assertEquals(coupon.total_odds(),3.0)
	
	def test_is_coupon_won(self):
		coupon=Coupon.objects.get(pk=1)
		self.assertEquals(coupon.is_coupon_won(),False)
	
	def test_is_stake_minimal(self):
		coupon=Coupon.objects.get(pk=1)
		self.assertEquals(coupon.is_stake_minimal(3.0),True)
		self.assertEquals(coupon.is_stake_minimal(0.22),False)		

	def test_get_odds(self):
		placedbet=PlacedBet.objects.get(pk=1)
		self.assertEquals(placedbet.get_odds(),2.00)	

	def test_setteama(self):
		bet=Bet.objects.get(pk=1)
		self.assertEquals(bet.set_teama('Legia'),True)
		self.assertEquals(bet.set_teama('Milan'),True)
		self.assertEquals(bet.set_teama(123),False)
	
	def test_setteamb(self):
		bet=Bet.objects.get(pk=1)
		self.assertEquals(bet.set_teamb('Legia'),True)
		self.assertEquals(bet.set_teamb('Milan'),True)
		self.assertEquals(bet.set_teamb(123),False)
	
	def test_setoddsa(self):
		bet=Bet.objects.get(pk=1)
		self.assertEquals(bet.set_oddsa(123),True)
		self.assertEquals(bet.set_oddsa(12.23),True)
		self.assertEquals(bet.set_oddsa("slowo"),False)
	
	def test_betslist_url(self):
		url=reverse('home')	
		self.assertEquals(resolve(url).func,show_bets_view)
	
	def test_addbet_url(self):
		url=reverse('addbet')	
		self.assertEquals(resolve(url).func,add_bet_view)
	
	def test_betslist_admin_url(self):
		url=reverse('betscores')		
		self.assertEquals(resolve(url).func,show_bets_to_admin)	

	def test_showcoupons_url(self):
		url=reverse('coupons')		
		self.assertEquals(resolve(url).func,show_bets_to_admin)	