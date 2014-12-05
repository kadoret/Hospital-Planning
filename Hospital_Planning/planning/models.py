from django.db import models
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.
from datetime import datetime
import datetime		
from django.conf import settings

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class reserved_days(models.Model):
	"""
	class reserved_days 
		Model contain days not allowed for planning
	"""	
	class Meta:
		unique_together=('day','pdoctor')
	
	day = models.DateField(auto_now=False, auto_now_add=False)
	pdoctor = models.ForeignKey(settings.AUTH_USER_MODEL)

class planning(models.Model):
	"""
	class planning 
		Main model, the planning
		planning -> job
		planning -> doctors
		planning -> timestamps
	"""	
	class Meta:
		unique_together=('ptimestamp','pjob','day')
	
	day = models.DateField(auto_now=False, auto_now_add=False, help_text=' Utiliser le format dd/mm/yyyy')
	official_approved =  models.BooleanField(default = True)
	request_swap = models.BooleanField(default = False) 
	
	pjob = models.ForeignKey('planning.jobs')
	pdoctor = models.ForeignKey(settings.AUTH_USER_MODEL)
	ptimestamp =  models.ForeignKey('planning.timestamps')
	
	request_swap_to = models.ManyToManyField('self', through='planning_swap', symmetrical=False)

	def save(self, *args, **kwargs):
		super(planning, self).save(*args, **kwargs)
		try:
			aPlanning_hist = planning_hist.objects.get(pplanning = self.id, current_version = True)
			if aPlanning_hist.pdoctor != self.pdoctor:
				aPlanning_hist.current_version = False
				aPlanning_hist.save()
				planning_hist.objects.create(pplanning_id = self.id, 
								ptimestamp = self.ptimestamp,
								pdoctor = self.pdoctor,
								pjob = self.pjob,
								current_version = True,
								version = int(aPlanning_hist.version) + 1,
								day = datetime.date.today())
		except ObjectDoesNotExist:
			planning_hist.objects.create(pplanning_id = self.id,
							ptimestamp = self.ptimestamp,
							pdoctor = self.pdoctor,
							pjob = self.pjob,
							current_version = True,
							version = 1,
							day = datetime.date.today())
			
class planning_hist(models.Model):
	"""
	class planning_hist 
		Histo of planning model
	"""	
	day = models.DateField(auto_now=False, auto_now_add=False)
	version = models.IntegerField()
	current_version = models.BooleanField(default = True)	

	pjob = models.ForeignKey('planning.jobs')
	pdoctor = models.ForeignKey(settings.AUTH_USER_MODEL)
	ptimestamp =  models.ForeignKey('planning.timestamps')
	pplanning = models.ForeignKey(planning)
	

class planning_swap(models.Model):
	"""
	class planning_swap 
		Join model with planning and doctors for swapping
	"""	
	planning_to_swap = models.ForeignKey(planning, related_name='planning_to_swap_set')
	doctor_to_swap = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctor_to_swap_set')
	planning_to_swap_with = models.ForeignKey(planning, related_name='planning_to_swap_with_set')
	doctor_to_swap_with = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctor_to_swap_with_set')
	date = models.DateField(auto_now=False, auto_now_add=False)
	accepted =  models.BooleanField(default = False)
	validated = models.BooleanField(default = False)
	

class MyDoctorManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not username:
			raise ValueError('Not user provided')

		user = self.model(
            username=username,
            email=email,
        )

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email,password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(username,
            password=password,
            email=email
        )
		user.is_admin = True
		user.save(using=self._db)
		return user


class timestamps(models.Model):
	"""
	class timestamps 
		Timestamps model
	"""	
	serial =  models.CharField(max_length = 15, unique=True)
	description =  models.CharField(max_length = 35)

	def __unicode__(self):
		return self.serial

	class Meta:
		verbose_name = 'Horaire de garde'
		verbose_name_plural = 'Horaires de garde'

class days(models.Model):
	"""
	class days 
		days model
		days -> (1 to n) timestamps
	"""	
	name = models.CharField(max_length = 25)
	timestamp =  models.ManyToManyField(timestamps)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Journee de garde'
		verbose_name_plural = 'Journees de garde'
		
class jobs(models.Model):
	"""
	class jobs 
		jobs model
		jobs -> (1 to n) jobs (needed to link jobs)
	"""	
	name = models.CharField(max_length = 50)
	serial =  models.CharField(max_length = 15, unique=True)
	day = models.ManyToManyField(days)
	linked_to = models.ManyToManyField('self', blank=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Poste de garde'
		verbose_name_plural = 'Postes de garde'


class doctors(AbstractBaseUser):
	"""
	class doctors 
		doctors model, the user model
	"""	
	email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=False,
    )
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	djobs = models.ManyToManyField(jobs)
	username =  models.CharField(max_length = 30, unique=True)

	objects = MyDoctorManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def __str__(self):              # __unicode__ on Python 2
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin






