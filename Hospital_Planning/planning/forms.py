from django import forms
from services.models import Users_Services,Services, UserHospital, Timestamps
from planning.models import Planning, Planning_Free
import datetime
from datetime import timedelta

class PlanningChangeForm(forms.Form):
	title = forms.CharField(max_length=20)
	message = forms.CharField(widget=forms.Textarea)
	# Dynamic change of choice, use a function instead of static list 
	users = forms.MultipleChoiceField(choices = [], widget=forms.CheckboxSelectMultiple)
	
	class UserSwap(object):
		def __init__(self, userhospitalmodel):
			for i in  vars(userhospitalmodel).keys():
				setattr(self, i, vars(userhospitalmodel)[i])

		def __str__(self):
			return 'user: '+ self.username+' date: '+ str(self.date) + ' time: ' + str(self.description) + ' service: ' + str(self.service)

		def __eq__(self, obj):
			return self.username == obj.username

		def date(self, date):
			#FIXME Get the service, mandatory !!!
			(day, timestamp) = date
			self.date = day
			self.description = Timestamps.objects.get(id = timestamp).description
			try:
				service_id = Planning.objects.filter(puser=self.id,day=day, ptimestamp=timestamp).values_list('pservice',flat=True)
				self.service = Services.objects.get(id = service_id[0] ).name
			except:
				pass
			return self
	
	def __init__(self, *args, **kwargs):	
		if ('user_id' and 'service_id' and 'timestamp_id' and 'day') in kwargs:
			current_user = kwargs['user_id']
			current_service = kwargs['service_id']
			current_timestamp = kwargs['timestamp_id']
			current_day = kwargs['day']
			super(PlanningChangeForm, self).__init__()
			users_choice = self.getUsersForChange(	current_user, 
								current_service, 
								current_day, 
								current_timestamp)
			self.fields['users'].choices = users_choice
		else:
			super(PlanningChangeForm, self).__init__(*args, **kwargs)

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
		# validate planning really exist
		try:
			Planning.objects.get(   pservice = current_service, 
					        day = current_day, 
						ptimestamp = current_timestamp, 
						puser = current_user)
		except:
			return [] 
		# users  of the  current service
		users_same_service = Users_Services.objects.filter( services=current_service
									).exclude(users=current_user
									).values_list('users',flat=True)
		# check user works
		users_working = Planning.objects.filter( pservice = current_service, 
							 day = current_day, 
							 ptimestamp = current_timestamp 
								).exclude(puser = current_user
										).values_list('puser',flat=True)
		# get all potentiel user who can swap their gard
		elegible_users =  [int(item) for item in set(users_same_service).difference(set(users_working))]
		# Now  take attention to the relation between each services, if services are linked (similar) ok you can swap!
		user_current_service = Services.objects.get(id = current_service)
		services_linked_list = [int(item) for item in user_current_service.linked_to.values_list('id', flat=True)]
		services_linked_list.append(int(current_service))
		# now get the date can change for the user and the elegible, do no take care about the services
		current_user_date_swap =  [ ( item1, int(item2)  ) for item1,item2,item3 in 
									Planning_Free.objects.filter( puser = current_user, 
										     		      day__range=[ datetime.date.today(), 
														   datetime.date.today() + timedelta( days = 360 ) ]
													).values_list('day','ptimestamp','pservice')
														if int(item3) in services_linked_list ]
		elegible_users_date_swap = {}
		for anElegibleUser in elegible_users:
			elegible_users_date_swap[str(anElegibleUser)] =  [ (item1, int(item2))  for item1,item2,item3 in 
													Planning.objects.filter(#pservice = current_service, 
																puser = anElegibleUser 	
																).values_list('day','ptimestamp','pservice')
																	if int(item3) in services_linked_list ]
		# final compute
		final = []
		for user_id in elegible_users_date_swap.keys():
			for adate in set(current_user_date_swap).intersection( set( elegible_users_date_swap[user_id] ) ):
				final.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = long(user_id))).date(adate))
		return final
