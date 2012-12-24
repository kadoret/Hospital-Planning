from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Planning(models.Model):
	class Meta:
		unique_together=('day','pcalandar','ptimestamp')
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	pservice = models.ForeignKey('calandars.Calandars')
	puser = models.ForeignKey(User)
	ptimestamp =  models.ForeignKey('calandars.Timestamps')
	request_change = models.BooleanField(default=1)

class Planning_Availability(models.Model):
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	puser = models.ForeignKey(User)

class Plannning_Change(models.Model):
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	puser = models.ForeignKey(User)
	pservice = models.ForeignKey('services.Services')
