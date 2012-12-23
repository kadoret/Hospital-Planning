from django.db import models

# Create your models here.
class Users(models.Model):
	class Meta:
		unique_together = ('lastname', 'firstname')
	lastname = models.CharField(max_length = 25)
	firstname =  models.CharField(max_length = 25)
	serial = models.CharField(max_length = 25)
	email = models.CharField(max_length = 25)
	calandars = models.ManyToManyField('calandars.Calandars',through='Users_Calandars')
	
	def __unicode__(self):
		return self.lastname 

class Hospital(models.Model):
	name = models.CharField(max_length = 25)
	adress =  models.CharField(max_length = 25)

	def __unicode__(self):
		return self.name

class Users_Calandars(models.Model):

	status =  models.IntegerField()
	calandar = models.ForeignKey('calandars.Calandars')
	user =  models.ForeignKey(Users)
	#TODO : def Unicode

class Acceptance(models.Model):
	user = models.ForeignKey(Users)
	weight = models.FloatField()
