from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from decimal import Decimal
# Create your models here.



class User(AbstractUser):
	is_customer=models.BooleanField(default=False)

	def __str__(self):
		return self.username

class Customer(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer")
	birth_date=models.DateField(verbose_name="birth_date",null=True,blank=True)
	money=models.DecimalField(max_digits=8, decimal_places=2,default=200)

	def over_eighteen(self):
		today=date.today() 
		age=today.year-self.birth_date.year-((today.month, today.day)<(self.birth_date.month, self.birth_date.day))
		if age>17:
			return True
		else:
			return False	

	def set_money(self,money):
		if isinstance(money,Decimal) or isinstance(money,float) or isinstance(money,int):
			self.money=money
			self.save()
			return True
		else:
			return False	

	def won_money(self,prize):
		if isinstance(prize,Decimal) or isinstance(prize,float) or isinstance(prize,int):
			return self.money+prize
		else:
			return self.money

	def deducted_money(self,stake):
		if isinstance(stake,Decimal) or isinstance(stake,float) or isinstance(stake,int):
			return self.money-stake
		else:
			return self.money

	def have_enough(self,stake):
		if isinstance(stake,Decimal) or isinstance(stake,float) or isinstance(stake,int):
			if self.money>=stake:
				return True
			else:
				return False
		else:
			return False		


	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	if instance.is_customer:
		Customer.objects.get_or_create(user = instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	print('_-----')	
	# print(instance.internprofile.bio, instance.internprofile.location)
	if instance.is_customer:
		instance.customer.save()	