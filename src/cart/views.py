from django.shortcuts import render,redirect,get_object_or_404
from account.models import User
from cart.models import Cart
from bets.views import show_bets_view
from django.urls import reverse
from decimal import Decimal
from django.contrib import messages
from bets.models import Coupon,Bet,PlacedBet
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/login')
def add_to_cart(request,betid):
	user_cart=get_object_or_404(Cart,user=request.user)
	bet=Bet.objects.filter(bet_id=betid).first()
	if bet in user_cart.bets.all():
		user_cart.bets.remove(bet)
		user_cart.save()
	else:
		user_cart.bets.add(bet)
		user_cart.save()
	return redirect('home')

	

@login_required(login_url='/login')
def add_coupon_view(request):
	if request.method=="POST":
		user_cart=get_object_or_404(Cart,user=request.user)
		user=request.user
		placedbets=[]
		if user_cart.bets.all():
			for bets in user_cart.bets.all():
				placedbettemp=PlacedBet(pick=request.POST.get(str(bets.bet_id)))
				placedbettemp.save()
				placedbettemp.bet_id.add(bets)	
				placedbettemp.save()		
				placedbets.append(placedbettemp)
				placedbettemp=0
			if request.POST.get("stake"):
				stake=Decimal(request.POST.get("stake"))
				if user.customer.have_enough(stake):		
					coupon=Coupon(user=user,stake=stake,is_placed=True,status=None)
					if coupon.is_stake_minimal(stake):
						coupon.save()		
						for placedbetsitem in placedbets:			
							coupon.placedbets.add(placedbetsitem) 
						coupon.save()
						user_cart.bets.clear()
						user.customer.money=user.customer.deducted_money(stake)
						user.customer.save()
						messages.success(request, 'Zaklad Dodany')
					else:
						messages.error(request, 'Stawka za mala')
				else:
					messages.error(request, 'Uzytkownik nie ma tyle pieniedzy')
			else: 
				messages.error(request, 'Prosze podac stawke')
		else: 
			messages.error(request, 'Pusty koszyk')
		return redirect('home')