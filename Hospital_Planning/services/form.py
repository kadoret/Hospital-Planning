from django import forms
from models import Services, Dates, Timestamps, UserHospital

class ServicesForm(forms.ModelForm):
	class Meta:
        	model =  Services

class DatesForm(forms.ModelForm):
	class Meta:
		model = Dates

class TimestampsForm(forms.ModelForm):
	class Meta:
		model = Timestamps
