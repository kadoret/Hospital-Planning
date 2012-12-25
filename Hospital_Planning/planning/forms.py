from django import forms
from services.models import Users_Services, UserHospital, Timestamps
import datetime
from datetime import timedelta

class PlanningChangeForm(forms.Form):
	title = forms.CharField(max_length=20)
	message = forms.CharField(widget=forms.Textarea)
	# Dynamic change of choice, use a function instead of static list 
	users = forms.MultipleChoiceField(choices = [], widget=forms.CheckboxSelectMultiple)
	
	class UserSwap(object):
		def __init__(self, userhospitalmodel):
			#TODO Find a better way : getAttribut with not callable ?
			self.id = userhospitalmodel.id
			self.username = userhospitalmodel.username
			self.first_name = userhospitalmodel.first_name
			self.last_name = userhospitalmodel.last_name
			self.email = userhospitalmodel.email

		def date(self, day):
			#TODO parsing horrible 
			self.date = day[0][0]
			self.description = Timestamps.objects.get(id=day[0][1]).description

	
	def __init__(self, *args, **kwargs):
		current_user = kwargs.pop['user_id']
		current_service = kwargs.pop['calandar_id']
		current_timestamp = kwargs.pop['timestamp_id']
		super(PlanningChangeForm, self).__init__(*args, **kwargs)
		users_choice = getUsersForChange(current_user, current_service, current_timestamp)
		self.fields['users'].choices = users_choice

	def requestPlanningSwap(self):
		"""
			Update the planning in order to inform their is a change request
			Send an internal email
			Send an mail of the selected users and the administrators
		"""	
		pass

	def getUsersForChange(self, current_user, current_service, current_day, current_timestamp):
		"""
			Return the elegible users depends on :
				- work or not
				- work in this service
			Return in priority the users want to exchange a days 
		"""
		# users  of the  current service
		user_serviceList = Users_Services.objects.filter(services=current_service).exclude(users=current_user).value_list('users',  flat=True)
		# check user works
		user_workList = Planning.objects.filter(pservice = current_service, day = current_day, ptimestamp = current_timestamp ).exclude(puser = current_user).values_list('puser',  flat=True)
		# get all potentiel user who can swap their gard
		elegible_user = set(user_serviceList).difference(set(user_workList))
		# now get the date can change
		# FIXME parameter for te range date ?
		dayList = Planning_Free.objects.filter(puser = current_user, day__range=[datetime.date.today(), datetime.date.today() + timedelta( days = 360 )]).values_list('day', 'ptimestamp',  flat=True)
		for anElegibleUser in elegible_user:
			ElegibleUser_date[anElegibleUser] =  Planning.objects.filter(pservice = current_service, puser = anElegibleUser ).values_list('day', 'ptimestamp', flat=True)
		# sort for each avalaible user the dates to changa
		finalist = [] 
		for key,value in ElegibleUser_date:
			for aday in set(dayList).intersection(set(value)):
				finalist.append(UserSwap(UserHospital.objects.get(id=key).date(aday)))
		return finalist
