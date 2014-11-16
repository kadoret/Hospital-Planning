from django import forms
from planning.extra.methods import UserSwap, getUserSwapForPlanningSwap, setPlanningSwap, handle_uploaded_planning
from planning.models import planning
import datetime
from datetime import timedelta



class PlanningForm(forms.ModelForm):
	class Meta:
		model = planning
		exclude = ('request_swap', 'official_approved', 'request_swap_to')
 

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
