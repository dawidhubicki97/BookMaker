from django.db import models
from bets.models import Bet
from account.models import User
# Create your models here.
class Cart(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="user")
	bets=models.ManyToManyField(Bet,blank=True)
	
