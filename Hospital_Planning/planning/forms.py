from django import forms
from planning.extra.methods import UserSwap, getUserSwapForPlanningSwap, setPlanningSwap
import datetime
from datetime import timedelta


class PlanningImportForm(forms.Form):
	"""
	"""
	file  = forms.FileField()
	#TODO ovveride is_valid()
		

class PlanningSwapForm(forms.Form):
	"""
	class PlanningSwapForm 
		Form for swapping a planning
	"""
	subject = forms.CharField( max_length = 20 )
	message = forms.CharField(widget=forms.Textarea)
	# Dynamic change of choice, use a function instead of static list 
	planning_swap = forms.MultipleChoiceField(choices = [], widget=forms.CheckboxSelectMultiple)
	def __init__(self, *args, **kwargs):
		""" override init method to get users to swap """
		doctor_id = kwargs.pop('doctor_id')
		planning_id = kwargs.pop('planning_id')	
		super(PlanningSwapForm, self).__init__(*args, **kwargs)
		users_choice = getUserSwapForPlanningSwap( current_user = doctor_id, planning_id = planning_id )
		self.fields['planning_swap'].choices = [ i.marshall() for i in users_choice ]

	def save(self, *args, **kwargs):
		""" override save method """
		setPlanningSwap(list_swap = self.cleaned_data['planning_swap'],
				subject = self.cleaned_data['subject'],
				text = self.cleaned_data['message'],
				planning_id = kwargs['planning_id'],
				current_user = kwargs['doctor_id'])
