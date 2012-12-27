from django import forms
import functions
from functions import UserSwap, getUserSwapForPlanningSwap, setPlanningSwap
import datetime
from datetime import timedelta

class PlanningSwapForm(forms.Form):
	"""

	"""
	title = forms.CharField(max_length=20)
	message = forms.CharField(widget=forms.Textarea)
	# Dynamic change of choice, use a function instead of static list 
	users = forms.MultipleChoiceField(choices = [], widget=forms.CheckboxSelectMultiple)
	
	def __init__(self, *args, **kwargs):
		""" override init method to get users to swap """	
		if ('user_id' and 'service_id' and 'timestamp_id' and 'day') in kwargs:
			current_user = kwargs['user_id']
			current_service = kwargs['service_id']
			current_timestamp = kwargs['timestamp_id']
			current_day = kwargs['day']
			super(PlanningSwapForm, self).__init__()
			# return list of 'swap' users
			users_choice = getUserSwapForPlanningSwap( current_user, 
							 	   current_service, 
							  	   current_day, 
							           current_timestamp)
			self.fields['users'].choices = users_choice
		else:
			super(PlanningSwapForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		""" override save method """
		setPlanningSwap()
