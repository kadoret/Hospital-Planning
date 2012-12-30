from django import forms
from planning.extra.methods import UserSwapField, UserSwap, getUserSwapForPlanningSwap, setPlanningSwap
import datetime
from datetime import timedelta


class PlanningSwapForm(forms.Form):
	"""
	class PlanningSwapForm 
		Form for swapping a planning
	"""
	title = forms.CharField( max_length = 20 )
	message = forms.CharField(widget=forms.Textarea)
	# Dynamic change of choice, use a function instead of static list 
	users = UserSwapField(choices = [], widget=forms.CheckboxSelectMultiple)
	def __init__(self, *args, **kwargs):
		""" override init method to get users to swap """
		user_id = kwargs.pop('user_id')
		planning_id = kwargs.pop('planning_id')	
		super(PlanningSwapForm, self).__init__(*args, **kwargs)
		users_choice = getUserSwapForPlanningSwap( current_user = user_id, planning_id = planning_id )
		self.fields['users'].choices = [ i.marshall() for i in users_choice ]

	def save(self, *args, **kwargs):
		""" override save method """
		setPlanningSwap(list_swap = self.fields['users'],
				title = self.fields['title'],
				text = self.fields['message'])
