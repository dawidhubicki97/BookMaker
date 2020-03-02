from django.test import TestCase
from account.models import User,Customer
from django.urls import reverse,resolve
from account.views import customer_profile_view, logout_view, login_view
from account.forms import UserForm,CustomerForm
from django.test.client import RequestFactory
import datetime 
from decimal import Decimal
    
# Create your tests here.
class BasicTestClass(TestCase):


	def setUp(self):
		user=User(username="testowy",email="costam@gmail.com")
		user.set_password("haslo123")
		user.is_admin=False
		user.is_active=True
		user.is_customer=True
		user.save()
		user.customer.birth_date=datetime.date(1997,10,1)
		user.customer.money=500.0
		user.customer.save()		

	def test_overeighteen(self):
		user=User.objects.get(pk=1)
		isover=user.customer.over_eighteen()
		self.assertEquals(isover,True)		

	def test_deductedmoney(self):
		user=User.objects.get(pk=1)
		self.assertEquals(user.customer.deducted_money(100),400)	
		self.assertEquals(user.customer.deducted_money(150),350)	
		self.assertEquals(user.customer.deducted_money(250),250)
		self.assertEquals(user.customer.deducted_money("asd"),500)	

	def test_wonmoney(self):
		user=User.objects.get(pk=1)
		self.assertEquals(user.customer.won_money(100),600)	
		self.assertEquals(user.customer.won_money(150),650)	
		self.assertEquals(user.customer.won_money(250),750)
		self.assertEquals(user.customer.won_money("asd"),500)	


	def test_haveenough(self):
		user=User.objects.get(pk=1)
		self.assertEquals(user.customer.have_enough(100),True)	
		self.assertEquals(user.customer.have_enough(150),True)	
		self.assertEquals(user.customer.have_enough(1250),False)
		self.assertEquals(user.customer.have_enough("asd"),False)		

	def test_setmoney(self):
		user=User.objects.get(pk=1)
		self.assertEquals(user.customer.set_money(321),True)
		self.assertEquals(user.customer.set_money(1231.3),True)		
		self.assertEquals(user.customer.set_money("napis"),False)		

	def test_register_url(self):
		url=reverse('register')	
		self.assertEquals(resolve(url).func,customer_profile_view)
	def test_logout_url(self):
		url=reverse('logout')	
		self.assertEquals(resolve(url).func,logout_view)
	def test_login_url(self):
		url=reverse('login')		
		self.assertEquals(resolve(url).func,login_view)	
	
	def test_registration_form_user_data(self):
		form=UserForm(data={'username':'dawid','email':'dawid@gmail.com','password1':123456,'password2':123456})	
		self.assertTrue(form.is_valid())
	def test_registration_form_customer_data(self):
		form=CustomerForm(data={'nickname':'przykladowa','birth_date':'1990-10-10'})	
		self.assertTrue(form.is_valid())
	def test_registration_form_user_nodata(self):
		form=UserForm(data={})	
		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors),3)
	def test_registration_form_customer_nodata(self):
		form=CustomerForm(data={})	
		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors),2)