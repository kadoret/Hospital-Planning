from django import forms

class PlanningChangeForm(forms.ModelForm):
	title = forms.Charfield(max_length=20)
	message = forms.CharField(widget=forms.Textarea)
	# Dynamic change of query set, use a function instead of query 
	users = forms.ModelMultipleChoiceField(queryset=User.objects.none())
	
	def __init__(self, *args, **kwargs):
		current_user = kwargs.pop['user_id']
		current_service = kwargs.pop['calandar_id']
		current_timestamp = kwargs.pop['timestamp_id']
		super(PlanningChangeForm, self).__init__(*args, **kwargs)
		users_choice = getUsersForChange(current_user, current_service, current_timestamp)
		self.fields['users'].queryset = users_choice

	def requestPlanningSwap(self):
		pass

	def getUsersForChange(self, current_user, current_service, current_timestamp):
		pass

