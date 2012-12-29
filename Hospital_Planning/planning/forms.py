from django import forms
from planning.extra.methods import UserSwap, getUserSwapForPlanningSwap, setPlanningSwap
import datetime
from datetime import timedelta

class PlanningSwapForm(forms.Form):
	"""

	"""
	title = forms.CharField( max_length = 20 )
	message = forms.CharField(widget=forms.Textarea)
	# Dynamic change of choice, use a function instead of static list 
	users = forms.MultipleChoiceField(choices = ['1','2'], widget=forms.CheckboxSelectMultiple)
	
	def __init__(self, *args, **kwargs):
		""" override init method to get users to swap """	
		if 'user_id' in kwargs and 'planning_id' in kwargs:
			super(PlanningSwapForm, self).__init__()
			# return list of 'swap' users
			users_choice = getUserSwapForPlanningSwap( kwargs['user_id'], kwargs['planning_id'] )
			self.fields['users'].choices = [ i.marshall() for i in users_choice ]
		else:
			super(PlanningSwapForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		""" override save method """
		setPlanningSwap()
