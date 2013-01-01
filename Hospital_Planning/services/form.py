from django import forms
from models import jobs, days, timestamps, doctors

class JobsForm(forms.ModelForm):
	class Meta:
        	model =  jobs

class DaysForm(forms.ModelForm):
	class Meta:
		model = days

class TimestampsForm(forms.ModelForm):
	class Meta:
		model = timestamps
