from django.db import models
from services.models import Users_Services, Services
# Create your models here.

class Import_Configuration(models.Model):
	name = models.CharField(max_length = 40, unique=True)
	services = models.ManyToManyField(Services)

class Planning_Free(models.Model):
	class Meta:
		unique_together=('day','ptimestamp','puser')
	day = models.DateField(auto_now=False, auto_now_add=False)
	pservice = models.ForeignKey('services.Services')
	ptimestamp =  models.ForeignKey('services.Timestamps')
	puser = models.ForeignKey('services.UserHospital')


class Planning(models.Model):
	class Meta:
		unique_together=('ptimestamp','puser','day')
	day = models.DateField(auto_now=False, auto_now_add=False)
	pservice = models.ForeignKey('services.Services')
	puser = models.ForeignKey('services.UserHospital')
	ptimestamp =  models.ForeignKey('services.Timestamps')
	request_change = models.BooleanField(default = False)

	def save(self, *args, **kwargs):
		super(Planning, self).save(*args, **kwargs)
		# like a proc on database
		other_user_list = Users_Services.objects.exclude(users_id = self.puser.id).filter(services_id = self.pservice.id)
		for user in other_user_list:
			Planning_Free.objects.create(day = self.day, pservice_id = self.pservice.id, ptimestamp_id = self.ptimestamp.id, puser_id = user.users_id)
