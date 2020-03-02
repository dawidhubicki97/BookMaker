from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from account.forms import UserForm,CustomerForm,AccountAuthenticationForm
from cart.models import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def customer_profile_view(request):
	
	if request.method == 'POST':		
		user_form = UserForm(request.POST,prefix='UF')
		profile_form = CustomerForm(request.POST,prefix='PF')		
		

		if user_form.is_valid() and profile_form.is_valid() and user_form.cleaned_data['password1'] == user_form.cleaned_data['password2'] and len(user_form.cleaned_data['password1'])>5:
			user = user_form.save(commit=False)		
			user.set_password(user_form.cleaned_data['password1'])	
			user.is_active=True
			user.is_customer=True
			user.save()
			user.customer.birth_date = profile_form.cleaned_data.get('birth_date')
			if user.customer.over_eighteen():
				user.customer.save()
				cart=Cart(user=user)
				cart.save()
				messages.success(request, 'Uzytkownik stworzony')
				return redirect('home')
			else: 
				user.delete()
				profile_form.add_error('birth_date', 'Nie masz 18 lat')
		elif user_form.cleaned_data['password1'] != user_form.cleaned_data['password2']:
			user_form.add_error('password2', 'Hasła nie są takie same')
		elif len(user_form.cleaned_data['password1'])<6:
			user_form.add_error('password1', 'Hasło za krótkie')

	else:
		user_form = UserForm(prefix='UF')
		profile_form = CustomerForm(prefix='PF')
		
	return render(request,'account/register.html',{
			'user_form': user_form,
			'profile_form': profile_form,
		})

@login_required(login_url='/login')
def logout_view(request):
	logout(request)
	return redirect('home')


def login_view(request):
	context={}
	user=request.user
	if user.is_authenticated:
		return redirect('home')

	if request.POST:
		form=AccountAuthenticationForm(request.POST)
		if form.is_valid():
			username=request.POST['username']
			password=request.POST['password']
			user=authenticate(username=username,password=password)

			if user:
				login(request,user)
				return redirect("home")
			else:
				form.add_error('password', 'Zly login lub haslo')
	else:
		form=AccountAuthenticationForm()

	context['login_form']=form
	return render(request,'account/login.html',context)
