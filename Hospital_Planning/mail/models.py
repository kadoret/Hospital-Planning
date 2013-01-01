from django.db import models
from services.models import doctors
# Create your models here.

class mail_adress(models.Model):
	email_intern = models.CharField(max_length = 50)
	muser = models.ForeignKey('services.doctors') 

class mail(models.Model):
	cuser = models.ForeignKey('services.doctors')
	subject = models.CharField(max_length = 50 )
	text = models.TextField()
	open = models.BooleanField(default=False)
	mfrom = models.ForeignKey(mail_adress)
