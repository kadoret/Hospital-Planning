from django.db import models

# Create your models here.

class Planning(models.Model):
	class Meta:
		unique_together=('day','pcalandar','ptimestamp')
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	pcalandar = models.ForeignKey('calandars.Calandars')
	puser = models.ForeignKey('users.Users')
	ptimestamp =  models.ForeignKey('calandars.Timestamps')

class Planning_Availability(models.Model):
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	puser = models.ForeignKey('users.Users')

class Plannning_Change(models.Model):
	day = models.DateTimeField(auto_now_add=True, auto_now=False)
	puser = models.ForeignKey('users.Users')
