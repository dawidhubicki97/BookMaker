from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from django.views.generic import View
import datetime
from pdfapp.utils import render_to_pdf 
from bets.models import Coupon,Bet,PlacedBet
from account.models import User,Customer

class GeneratePdf(View):

	def get(self, request, *args, **kwargs):
		won=0
		lost=0

		for coupon in Coupon.objects.all().iterator():
			if coupon.status==True:
				won=won+(coupon.stake*coupon.total_odds())
			elif coupon.status==False:
				lost=lost+coupon.stake	
		
		arrayusers=[]	
		for user in User.objects.all().iterator():
			wonuser=0
			lostuser=0
			for coupon in Coupon.objects.filter(user=user).iterator():
				if coupon.status==True:
					wonuser=wonuser+(coupon.stake*coupon.total_odds())
				elif coupon.status==False:
					lostuser=lostuser+coupon.stake	
			tempuserobject={
			'user':user,
			'wonuser':wonuser,
			'lostuser':lostuser}
			arrayusers.append(tempuserobject)		
			
		data = {
			'won': won, 
			'lost': lost,
			'arrayusers':arrayusers
		}	
		
		pdf = render_to_pdf('pdfapp/invoice.html', data)
		return HttpResponse(pdf, content_type='application/pdf')