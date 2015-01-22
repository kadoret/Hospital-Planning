from django import forms
from planning.extra.methods import getUserSwapForPlanningSwap, setPlanningSwap, handle_uploaded_planning
from planning.models import planning,jobs,days,timestamps
import datetime
from datetime import timedelta
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton                                               
from crispy_forms.layout import Layout, HTML, Submit
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm):
	"""
	class LoginForm 
		Form for login to the site
	"""	

	def __init__(self, *args, **kwargs):                                                   
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Identifiant'
		
	def is_valid(self, *args, **kwargs):
		request = kwargs.pop('request')
		super(LoginForm, self).is_valid(*args, **kwargs)
		if 'old_password' in request.POST:
			user = authenticate(username= request.user,
						password=request.POST['old_password'] )
		else:
			user = authenticate(username= self.request['username'], 
					password=self.request['password'] )
		if user is not None:
			if user.is_active:
				login(request, user)
				return True
		return False

class JobsForm(forms.ModelForm):
	class Meta:
		model = jobs
		#exclude = ('request_swap', 'official_approved', 'request_swap_to')

		labels = {
			'name': _('Service'),
			'serial': _('Identifiant'),
			'day': _('Jour'),
			'linked_to': _('Links'),
		}
	def __init__(self, *args, **kwargs):                                                   
		super(JobsForm, self).__init__(*args, **kwargs) 
		
class DaysForm(forms.ModelForm):
	class Meta:
		model = days
		#exclude = ('request_swap', 'official_approved', 'request_swap_to')

		labels = {
			'name': _('Jour'),
			'timestamp': _('Tranche horaire'),
		}
	def __init__(self, *args, **kwargs):                                                   
		super(DaysForm, self).__init__(*args, **kwargs) 

class TimestampsForm(forms.ModelForm):
	class Meta:
		model = timestamps
		#exclude = ('request_swap', 'official_approved', 'request_swap_to')

		labels = {
			'serial': _('Identifiant'),
			'description': _('Description'),
		}
	def __init__(self, *args, **kwargs):                                                   
		super(TimestampsForm, self).__init__(*args, **kwargs)
							
class PlanningForm(forms.ModelForm):
	"""
	class PlanningForm
		Form to planning
	"""

	class Meta:
		model = planning
		exclude = ('request_swap', 'official_approved', 'request_swap_to')
		widgets = {
			'day': forms.DateInput(format='%Y/%m/%d', attrs={'class':'dateinput'}),
		}
		labels = {
			'day': _('Jour'),
			'pjob': _('Service'),
			'pdoctor': _('Docteur'),
			'ptimestamp': _('Matin/Midi/Soir'),
		}
	def is_valid(self, *args, **kwargs):
		print self.fields['day']
		return True	
	def __init__(self, *args, **kwargs):                                                   
		super(PlanningForm, self).__init__(*args, **kwargs) 

class PlanningImportForm(forms.Form):
	"""
	class PlanningImportForm
		Form to import csv data
	"""
	file  = forms.FileField()
	#TODO overide is_valid()

	def save(self, *args, **kwargs):
		return handle_uploaded_planning(kwargs['file'])
		

class PlanningSwapForm(forms.Form):
	"""
	class PlanningSwapForm 
		Form for swapping a planning
	"""
	# Dynamic change of choice, use a function instead of static list 
	planning_swap = forms.MultipleChoiceField(choices = [], widget=forms.SelectMultiple(attrs={'class':'input-xxlarge', 'size':'30'}))
	
	def __init__(self, *args, **kwargs):
		""" override init method to get users to swap """
		doctor_id = kwargs.pop('doctor_id')
		planning_id = kwargs.pop('planning_id')	
		super(PlanningSwapForm, self).__init__(*args, **kwargs)
		users_choice = getUserSwapForPlanningSwap( current_user = doctor_id, planning_id = planning_id )
		list_choice = {}
		for user_choice in users_choice:
			key = str( user_choice.date) + ' ('+user_choice.description+ ')'
			if key in list_choice:
				list_choice[key].append( (str(user_choice.planning_swap), 
								user_choice.service_desc + ' : '+user_choice.username)
											)
			else:
				list_choice[key] = [ (str(user_choice.planning_swap),
										 user_choice.service_desc + ' : '+user_choice.username)]
			
		final_list = []
		for iterator in list_choice:
			final_list.append( (iterator, tuple(list_choice[iterator])) )
		#self.fields['planning_swap'].choices = [ i.marshall() for i in users_choice ]
		self.fields['planning_swap'].choices = final_list		

	def save(self, *args, **kwargs):
		""" override save method """
		setPlanningSwap(list_swap = self.cleaned_data['planning_swap'],
				planning_id = kwargs['planning_id'],
				current_user = kwargs['doctor_id'])
