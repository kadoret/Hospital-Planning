from services.models import doctors_jobs, doctors, timestamps, jobs
from planning.models import planning, planning_swap
from mail.models import mail_adress, mail
from django import forms
import datetime
from datetime import timedelta
import csv, re
from django.core.exceptions import ObjectDoesNotExist 
from django.db import IntegrityError

#TODO Handle re-entrance
def handle_uploaded_planning(f):
	""" will import the planning from csv to the database """
	try:
		data_rows = csv.reader(f, delimiter=';',  quoting=csv.QUOTE_NONE)
		cpt_header = True
		mapping = {}
		date_match = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{4}")
		for row in data_rows:
			cpt = 0
			date_planning = None
			# parsing the header
			if cpt_header:
				header = row
				# get the column
				for value in header:
					# ignore date
					data = value.strip()
					data = data.strip('"')
					data = data.strip('\'')
					keys = data.split('_')
					# ignore date and empty case
					if len(keys) == 2:
						mapping[str(cpt)] = ( jobs.objects.get(serial__iexact = keys[0] ),
									timestamps.objects.get(serial__iexact = keys[1]  ) )
						cpt_header = False
					cpt = cpt + 1
			else:
				# go through the planning
				for value in row:
					aDoctor = value.strip()
					aDoctor = aDoctor.strip('"')
					aDoctor = aDoctor.strip('\'')
					try:
						# No data some time it's happena
						if aDoctor != '' and date_planning is not None:
							planning.objects.create(day = datetime.datetime.strptime(date_planning, '%d/%m/%Y'),
									pdoctor = doctors.objects.get(username__iexact = aDoctor),
									pjob = mapping[str(cpt)][0] ,
									ptimestamp = mapping[str(cpt)][1] )
				
						elif  date_match.match(aDoctor) is not None:
							date_planning = aDoctor								

					except ObjectDoesNotExist, e:
						pass
					#	return False
					except IntegrityError, e:
						pass
						# Duplicate case
					#	return False
					cpt = cpt + 1
		return True		
	except ObjectDoesNotExist, e:
		return False

class planning_populate(object):

	def __init__(self, type_gen, jobs, day_range):
		self.type_gen = type_gen
		self.jobs = jobs
		self.day_range = day_range

	def _simple_constraint_generator(self):
		pass		

	def _constraint_generator(self):
		pass

	def _random_generator(self):
		pass

	def process(self):
		if self.type == 'simple':
			return self._simple_constraint_generator() 
		elif self.type == 'constainte':
			return self._constraint_generator()
		else:
			return self._random_generator()

class UserSwap(object):

 	def __init__(self, doctor_model):
		for i in vars(doctor_model).keys():
			setattr(self, i, vars(doctor_model)[i])
 
	def __str__(self):
		return ' '.join([self.username,
				 '-',    str(self.date),
				 '(',    self.description, 
				 ')', str(self.service_desc)])

	def __unicode__(self):
		return ' '.join([self.username,
				 '-',    str(self.date),
				 '(',    str(self.description),
				 ')', str(self.service_desc)])
	def __eq__(self, obj):
		return self.username == obj.username

	def marshall(self):
		return  (str(self.planning_swap), str(self)) 	
	
	def setSwapInfo(self, date, planning_id):
		try:
			(day, timestamp) = date
			self.date = day
			self.description = timestamps.objects.get(id = timestamp).description
			service_id = planning.objects.filter(
							pdoctor = self.id, day = day, ptimestamp = timestamp
								).values_list('pjob', flat=True)
			self.service_desc = jobs.objects.get(id = service_id[0] ).name
			self.planning_swap  = int(planning.objects.get( pdoctor = self.id,
									 pjob = service_id,
									 ptimestamp = timestamp,
									 day =day).id)
			return self
		except:
			return self

def setPlanningSwap(list_swap, subject, text, current_user, planning_id):
	""" Flag all the planning to be swap """  
	for planning_id_swap  in list_swap:
		user_swap = planning.objects.get(id = planning_id_swap).id
		planning_swap.objects.create(planning_to_swap = planning.objects.get(id = planning_id ),
						doctor_to_swap = doctors.objects.get(id = current_user ),
						planning_to_swap_with = planning.objects.get(id =planning_id_swap),
						doctor_to_swap_with = doctors.objects.get(id = user_swap),
						date = datetime.date.today())
		mail.objects.create(cuser = doctors.objects.get(id = user_swap),
				 subject = subject,
				 text = text,
				 mfrom = mail_adress.objects.get(
						muser = doctors.objects.get(id = current_user )))

def getUserSwapForPlanningSwap(current_user, planning_id):
	""" Return list of UserSwap for a specific planning swap """
	# validate planning really exist
	try:
		planning_swap = planning.objects.get( id = planning_id )
		# try to hack ...
		if planning_swap.pdoctor_id != current_user:
			return []
	except:
		return [] 
	# users  of the  current service
	users_same_job = doctors_jobs.objects.filter( jobs = planning_swap.pjob_id
								).exclude(doctors = planning_swap.pdoctor_id
								).values_list('doctors',flat=True)
	# check user works
	users_working = planning.objects.filter( pjob = planning_swap.pjob_id, 
						 day = planning_swap.day, 
						 ptimestamp = planning_swap.ptimestamp_id 
							).exclude(pdoctor = planning_swap.pdoctor_id
									).values_list('pdoctor',flat=True)
	# get all potentiel user who can swap their gard
	elegible_users =  [int(item) 
				for item in set(users_same_job).difference( set(users_working) )]
	# now  take attention to the relation between each jobs, if jobs are linked (similar) ok you can swap!
	user_current_job = jobs.objects.get(id = planning_swap.pjob_id)
	jobs_linked_list = [ int(item) 
					for item in user_current_job.linked_to.values_list('id', flat=True) ]
	jobs_linked_list.append(int(planning_swap.pjob_id))
	# now get the dates we can swap for the user, we check that the service is elegible. Store result in a set
#	current_user_date_swap =  [ ( item1, int(item2)  ) 
#					for item1,item2,item3 in 
#						availabilities.objects.filter
#									( pdoctor = current_user, 
#									  day__range= [ datetime.date.today(), 
#									  		datetime.date.today() + timedelta( days = 360 ) ]
#									).values_list('day','ptimestamp','pjob')
#						if int(item3) in jobs_linked_list ]
	current_user_none_date_swap = [ ( item1, int(item2)  )
						for item1,item2,item3 in
							planning.objects.filter
									( pdoctor = current_user,
										day__range= [ datetime.date.today(),
												datetime.date.today() + timedelta( days = 360 ) ]
									).values_list('day','ptimestamp','pjob') ]
#							if int(item3) in jobs_linked_list ]

	# now get the dates we can swap for the other user, we check that the service is elegible. Store result in a dic set
	elegible_users_date_swap = {}
	for anElegibleUser in elegible_users:
		elegible_users_date_swap[ str(anElegibleUser) ] =  [ (item1, int(item2))  
									for item1,item2,item3 in 
										planning.objects.filter( pdoctor = anElegibleUser 	
													).values_list('day','ptimestamp','pjob')
										if int(item3) in jobs_linked_list ]
	# we perfome set diff between the user as refrence and the other users
	final = []
	for user_id in elegible_users_date_swap.keys():
		for aSwapInfo in set(elegible_users_date_swap[user_id]).difference( set( current_user_none_date_swap ) ):
#		for aSwapInfo in set(current_user_date_swap).intersection( set( elegible_users_date_swap[user_id] ) ):
			#tricky it's the garanty for having 2 job complient 
			if planning.objects.filter(pdoctor_id = user_id, day = aSwapInfo[0], ptimestamp_id = aSwapInfo[1]
							).values_list('pjob_id', flat=True)[0] in jobs_linked_list: 
				final.append( 
					UserSwap( 
						doctors.objects.get(id = long(user_id))
						).setSwapInfo(aSwapInfo, planning_id) )
	return final
