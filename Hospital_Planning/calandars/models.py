from django.db import models

# Create your models here.

class Timestamps(models.Model):
        serial =  models.CharField(max_length = 15)
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

class Calandars(models.Model):
	description = models.CharField(max_length = 50)
	service =  models.CharField(max_length = 15)
	serial =  models.CharField(max_length = 15)
	day = models.ManyToManyField(Days)

	def __unicode__(self):
		return self.service
