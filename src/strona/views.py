from django.shortcuts import render
from account.models import User
# Create your views here.
def home_screen_view(request):
	
	context={}
	accounts=User.objects.all()
	context['accounts']=accounts
	
	return render(request,"strona/home.html",context)