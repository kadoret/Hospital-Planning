from django.db import models
from services.models import jobs
# Create your models here.

		

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
	
	pjob = models.ForeignKey('services.jobs')
	pdoctor = models.ForeignKey('services.doctors')
	ptimestamp =  models.ForeignKey('services.timestamps')
	
	request_swap_to = models.ManyToManyField('self', through='planning_swap', symmetrical=False)

#	def save(self, *args, **kwargs):
#		super(planning, self).save(*args, **kwargs)
		# like a proc on database
#		other_doctor_list = doctors_jobs.objects.exclude(
#								doctors_id = self.pdoctor.id).filter(
#									jobs_id = self.pjob.id)

#		for doctor in other_doctor_list:
#			availabilities.objects.create(day = self.day,
#					     pjob_id = self.pjob.id,
#					     ptimestamp_id = self.ptimestamp.id, 
#					     pdoctor_id = doctor.doctors_id)

#	def delete(self, *args, **kwargs):
#		super(planning, self).delete(*args, **kwargs)
#		availabilities.objects.create(day = self.day,
#						pjob_id = self.pjob.id,
#						ptimestamp_id = self.ptimestamp.id,
#						pdoctor_id = self.doctors.id)

#	def update(**kwargs):
#		availabilities.objects.create(day = self.day,
#						pjob_id = self.pjob.id,
#						ptimestamp_id = self.ptimestamp.id,
#						pdoctor_id = self.doctors.id)
#		super(planning, self).update(**kwargs)
#		availabilities.objects.get(day = self.day,
#						pjob_id = self.pjob.id,
#						ptimestamp_id = self.ptimestamp.id,
#						pdoctor_id = self.doctors.id).delete()

class planning_histo(models.Model):
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
