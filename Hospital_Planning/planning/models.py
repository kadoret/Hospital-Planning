from django.db import models
from services.models import doctors_jobs, jobs
# Create your models here.

class import_planning_configuration(models.Model):
	name = models.CharField(max_length = 40, unique=True)
	jobs = models.ManyToManyField(jobs)

	def __unicode__(self):
		return self.name

class availabilities(models.Model):
	class Meta:
		unique_together=('day','ptimestamp','pjob', 'pdoctor')
	
	day = models.DateField(auto_now=False, auto_now_add=False)

	pjob = models.ForeignKey('services.jobs')
	ptimestamp =  models.ForeignKey('services.timestamps')
	pdoctor = models.ForeignKey('services.doctors')
	

class planning(models.Model):
	class Meta:
		unique_together=('ptimestamp','pjob','day')
	
	day = models.DateField(auto_now=False, auto_now_add=False)
	official_approved =  models.BooleanField()
	
	pjob = models.ForeignKey('services.jobs')
	pdoctor = models.ForeignKey('services.doctors')
	ptimestamp =  models.ForeignKey('services.timestamps')
	
	request_swap_to = models.ManyToManyField('self')

	def save(self, *args, **kwargs):
		super(planning, self).save(*args, **kwargs)
		# like a proc on database
		other_doctor_list = doctors_jobs.objects.exclude(
								doctors_id = self.pdoctor.id).filter(
								jobs_id = self.pjob.id)
		for doctor in other_doctor_list:
			availabilities.objects.create(day = self.day,
					     pjob_id = self.pjob.id,
					     ptimestamp_id = self.ptimestamp.id, 
					     pdoctor_id = doctor.doctors_id)
