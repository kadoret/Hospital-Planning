from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Planning(models.Model):
	class Meta:
		unique_together=('day','pservice','ptimestamp')
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	pservice = models.ForeignKey('services.Services')
	puser = models.ForeignKey('services.UserHospital')
	ptimestamp =  models.ForeignKey('services.Timestamps')
	request_change = models.BooleanField(default=1)

class Planning_Availability(models.Model):
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	puser = models.ForeignKey('services.UserHospital')

class Plannning_Change(models.Model):
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	puser = models.ForeignKey('services.UserHospital')
	pservice = models.ForeignKey('services.Services')
