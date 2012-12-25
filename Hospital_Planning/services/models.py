from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
# Create your models here.

class Timestamps(models.Model):
        serial =  models.CharField(max_length = 15, unique=True)
        start =  models.CharField(max_length = 4)
        stop =  models.CharField(max_length = 4)

        def __unicode__(self):
                return self.serial

class Days(models.Model):
        day = models.IntegerField()
        name = models.CharField(max_length = 15)
        timestamp =  models.ManyToManyField(Timestamps)

        def __unicode__(self):
                return self.name

class Services(models.Model):
	description = models.CharField(max_length = 50)
	name =  models.CharField(max_length = 15)
	serial =  models.CharField(max_length = 15, unique=True)
	day = models.ManyToManyField(Days)

	def __unicode__(self):
		return self.name

class UserHospital(User):
	services = models.ManyToManyField(Services)
	objects = UserManager()

class UserHospitalAuthBackend(ModelBackend):
	def authenticate(self, username=None, password=None):
		try:
			user = self.user_class.objects.get(username = username)
			if user.check_password(password):
				return user
		except self.user_class.DoesNotExist:
			return None
		return None

	def get_user(self, user_id):
		try:
			return self.user_class.objects.get(pk = user_id)
		except self.user_class.DoesNotExist:
			return None
		return None

	@property
	def user_class(self):
		if not hasattr(self, '_user_class'):
			self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
			if not self._user_class:
				raise ImproperlyConfigured("Not OK")
		return self._user_class	

