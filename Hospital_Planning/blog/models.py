from django.db import models
from services.models import doctors

# Create your models here.
class blog(models.Model):
	bdoctor = models.ForeignKey('services.doctors')
	day = models.DateField(auto_now=False, auto_now_add=False)
	text = models.TextField()
