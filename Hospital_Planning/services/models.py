from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
# Create your models here.

class timestamps(models.Model):
        serial =  models.CharField(max_length = 15, unique=True)
	description =  models.CharField(max_length = 35)

        def __unicode__(self):
                return self.serial

	class Meta:
		verbose_name = 'Horaire de garde'
		verbose_name_plural = 'Horaires de garde'

class days(models.Model):
        name = models.CharField(max_length = 25)
        timestamp =  models.ManyToManyField(timestamps)

        def __unicode__(self):
                return self.name

	class Meta:
		verbose_name = 'Journee de garde'
		verbose_name_plural = 'Journees de garde'

class jobs(models.Model):
	name = models.CharField(max_length = 50)
	serial =  models.CharField(max_length = 15, unique=True)
	day = models.ManyToManyField(days)
	linked_to = models.ManyToManyField('self', blank=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Poste de garde'
		verbose_name_plural = 'Postes de garde'

class doctors(User):
#	djob = models.ManyToManyField(jobs, through='doctors_jobs')
	djobs = models.ManyToManyField(jobs)
	objects = UserManager()

	class Meta:
		verbose_name = 'Docteur'
		verbose_name_plural = 'Docteurs'

#class doctors_jobs(models.Model):
#	doctors = models.ForeignKey(doctors)
#	jobs =  models.ForeignKey(jobs)
#	status =  models.IntegerField()
#
#	def __unicode__(self):
#		return self.doctors.username + ' ' + self.jobs.name

#	class Meta:
#		verbose_name = 'Assignation des gardes'
#		verbose_name_plural = 'Assignation des gardes'

class doctors_auth_backend(ModelBackend):
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

