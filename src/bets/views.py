from django.shortcuts import render,redirect
from bets.forms import BetForm
from bets.models import Bet,Coupon,PlacedBet
from cart.models import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/login')
def show_bets_view(request):
	context={}
	context['bets']=Bet.objects.filter(finalscore="0").order_by('game_date')
	currentuser=request.user
	carti=Cart.objects.filter(user=currentuser)
	cartitems=carti[0].bets.all()
	context['cart']=cartitems	
	return render(request,"bets/betslist.html",context)
@login_required(login_url='/login')
def show_bets_view_category(request,category):
	context={}
	context['bets']=Bet.objects.filter(finalscore="0",category=category).order_by('game_date')	
	currentuser=request.user
	carti=Cart.objects.filter(user=currentuser)
	cartitems=carti[0].bets.all()
	context['cart']=cartitems	
	return render(request,"bets/betslistcategory.html",context)


@login_required(login_url='/login')
def show_coupons_view(request):
	context={}
	currentuser=request.user
	coupons=Coupon.objects.filter(user=currentuser)
	context['coupons']=coupons
	return render(request,"bets/couponslist.html",context)

@login_required(login_url='/login')
def show_bets_to_admin(request):
	context={}
	context['bets']=Bet.objects.filter(finalscore="0")
	return render(request,"bets/adminbetslist.html",context)

@login_required(login_url='/login')
def enter_score(request,betid):
	if request.method=="POST":
		bet=Bet.objects.filter(bet_id=betid).first()
		pick=request.POST.get(str(bet.bet_id))
		bet.finalscore=pick
		bet.save()
		placedbet=PlacedBet.objects.filter(bet_id=bet).first()
		if placedbet:
			for templacedbet in PlacedBet.objects.filter(bet_id=bet).iterator():
				if templacedbet.pick==pick:
					templacedbet.is_won=True
				else:
					templacedbet.is_won=False	
				templacedbet.save()
				#coupons=Coupon.objects.filter(placedbets=templacedbet)
				for tempcoupon in Coupon.objects.filter(placedbets=templacedbet).iterator():
					tempcoupon.is_coupon_won()
		cart=Cart.objects.filter(bets=bet).first()
		if cart:
			for tempcart in Cart.objects.filter(bets=bet).iterator():
				tempcart.bets.clear()
				tempcart.save()
					
	return redirect('betscores')
@login_required(login_url='/login')
def add_bet_view(request):
	if request.method=="POST":
		bet_form=BetForm(request.POST)
		if bet_form.is_valid() and bet_form.cleaned_data['oddsa']>=1 and bet_form.cleaned_data['oddsb']>=1 and bet_form.cleaned_data['oddsx'] >=1:
			bet=bet_form.save(commit=False)
			if bet.is_in_future():
				bet.save()
				messages.success(request, 'Mecz Dodany')
			else:
				bet_form.add_error('game_date', 'Data musi byc z przyszlosci')
		elif bet_form.cleaned_data['oddsa']<1:
			bet_form.add_error('oddsa', 'Kurs musi byc powyzej 1')
		elif bet_form.cleaned_data['oddsb']<1:
			bet_form.add_error('oddsb', 'Kurs musi byc powyzej 1')
		elif bet_form.cleaned_data['oddsx']<1:
			bet_form.add_error('oddsx', 'Kurs musi byc powyzej 1')
	else:
		bet_form=BetForm()

	return render(request,'bets/addbet.html',{
			'bet_form': bet_form,
			
		})

