from services.models import Users_Services,Services, UserHospital, Timestamps
from planning.models import Planning, Planning_Free
import datetime
from datetime import timedelta


class PlanningPopulate(object):

	def __init__(self, type_gen, services, day_range):
		self.type_gen = type_gen
		self.services = services
		self.day_range = day_range

	def _basic_generator(self):
		pass		

	def _constrainte_generator(self):
		pass

	def process(self):
		if self.type == 'simple':
			return self._basic_generator() 
		elif self.type == 'constainte':
			return self._constrainte_generator()

class UserSwap(object):

 	def __init__(self, userhospitalmodel):
		for i in vars(userhospitalmodel).keys():
			setattr(self, i, vars(userhospitalmodel)[i])
 
	def __str__(self):
		return ' '.join([self.username,
				 '-',    str(self.date),
				 '(',    str(self.description), 
				 ')', str(self.service_desc)])

	def __unicode__(self):
		return ' '.join([self.username,
				 '-',    str(self.date),
				 '(',    str(self.description),
				 ')', str(self.service_desc)])
	def __eq__(self, obj):
		return self.username == obj.username

	def marshall(self):
		return  ( (self.planning_swap_init, self.planning_swap_dest), self) 	
	
	def setSwapInfo(self, date, planning_id):
		try:
			(day, timestamp) = date
			self.date = day
			self.description = Timestamps.objects.get(id = timestamp).description
			service_id = Planning.objects.filter(
							puser = self.id, day = day, ptimestamp = timestamp
								).values_list('pservice', flat=True)
			self.service_desc = Services.objects.get(id = service_id[0] ).name
			self.planning_swap_init  = int(planning_id) 
			self.planning_swap_dest  = int(Planning.objects.get( puser = self.id, pservice = service_id, ptimestamp = timestamp, day =day).id)
			return self
		except:
			return self

def setPlanningSwap():
	""" Update the planning after a swap """
	pass

def getUserSwapForPlanningSwap(current_user, planning_id):
	""" Return list of UserSwap for a specific planning swap """
	# validate planning really exist
	try:
		planning_swap = Planning.objects.get( id = planning_id )
		# try to hack ...
		if planning_swap.puser_id != current_user:
			return []
	except:
		return [] 
	# users  of the  current service
	users_same_service = Users_Services.objects.filter( services = planning_swap.pservice_id
								).exclude(users= planning_swap.puser_id
								).values_list('users',flat=True)
	# check user works
	users_working = Planning.objects.filter( pservice = planning_swap.pservice_id, 
						 day = planning_swap.day, 
						 ptimestamp = planning_swap.ptimestamp_id 
							).exclude(puser = planning_swap.puser_id
									).values_list('puser',flat=True)
	# get all potentiel user who can swap their gard
	elegible_users =  [int(item) 
				for item in set(users_same_service).difference( set(users_working) )]
	# now  take attention to the relation between each services, if services are linked (similar) ok you can swap!
	user_current_service = Services.objects.get(id = planning_swap.pservice_id)
	services_linked_list = [ int(item) 
					for item in user_current_service.linked_to.values_list('id', flat=True) ]
	services_linked_list.append(int(planning_swap.pservice_id))
	# now get the dates we can swap for the user, we check that the service is elegible. Store result in a set
	current_user_date_swap =  [ ( item1, int(item2)  ) 
					for item1,item2,item3 in 
						Planning_Free.objects.filter
									( puser = current_user, 
									  day__range= [ datetime.date.today(), 
									  		datetime.date.today() + timedelta( days = 360 ) ]
									).values_list('day','ptimestamp','pservice')
						if int(item3) in services_linked_list ]
	# now get the dates we can swap for the other user, we check that the service is elegible. Store result in a dic set
	elegible_users_date_swap = {}
	for anElegibleUser in elegible_users:
		elegible_users_date_swap[ str(anElegibleUser) ] =  [ (item1, int(item2))  
									for item1,item2,item3 in 
										Planning.objects.filter( puser = anElegibleUser 	
													).values_list('day','ptimestamp','pservice')
										if int(item3) in services_linked_list ]
	# we perfome set diff between the user as refrence and the other users
	final = []
	for user_id in elegible_users_date_swap.keys():
		for aSwapInfo in set(current_user_date_swap).intersection( set( elegible_users_date_swap[user_id] ) ):
			final.append( 
				UserSwap( 
					UserHospital.objects.get(id = long(user_id))
					).setSwapInfo(aSwapInfo, planning_id) )
	return final
