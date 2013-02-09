from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from services.models import jobs
# Create your models here.
from datetime import datetime
import datetime		

class reserved_days(models.Model):
	class Meta:
		unique_together=('day','pdoctor')
	
	day = models.DateField(auto_now=False, auto_now_add=False)

	pdoctor = models.ForeignKey('services.doctors')

class planning(models.Model):
	class Meta:
		unique_together=('ptimestamp','pjob','day')
	
	day = models.DateField(auto_now=False, auto_now_add=False)
	official_approved =  models.BooleanField(default = True)
	request_swap = models.BooleanField(default = False) 
	
	pjob = models.ForeignKey('services.jobs')
	pdoctor = models.ForeignKey('services.doctors')
	ptimestamp =  models.ForeignKey('services.timestamps')
	
	request_swap_to = models.ManyToManyField('self', through='planning_swap', symmetrical=False)

	def save(self, *args, **kwargs):
		super(planning, self).save(*args, **kwargs)
		try:
			aPlanning_hist = planning_hist.objects.get(pplanning = self.id, current_version = True)
			if aPlanning_hist.pdoctor != self.pdoctor:
				aPlanning_hist.current_version = False
				aPlanning_hist.save()
				planning_hist.objects.create(pplanning = self.id, 
								ptimestamp = self.ptimestamp,
								pdoctor = self.pdoctor,
								pjob = self.pjob,
								current_version = True,
								version = int(aPlanning_hist.version) + 1,
								day = datetime.date.today())
		except ObjectDoesNotExist, e:
			#First creation
			pass
			

class planning_hist(models.Model):
	day = models.DateField(auto_now=False, auto_now_add=False)
	version = models.IntegerField()
	current_version = models.BooleanField(default = True)	

	pjob = models.ForeignKey('services.jobs')
	pdoctor = models.ForeignKey('services.doctors')
	ptimestamp =  models.ForeignKey('services.timestamps')
	pplanning = models.ForeignKey(planning)
	

class planning_swap(models.Model):
	planning_to_swap = models.ForeignKey(planning, related_name='planning_to_swap_set')
	doctor_to_swap = models.ForeignKey('services.doctors', related_name='doctor_to_swap_set')
	planning_to_swap_with = models.ForeignKey(planning, related_name='planning_to_swap_with_set')
	doctor_to_swap_with = models.ForeignKey('services.doctors', related_name='doctor_to_swap_with_set')
	date = models.DateField(auto_now=False, auto_now_add=False)
	accepted =  models.BooleanField(default = False)
