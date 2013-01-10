"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from planning.forms import PlanningSwapForm
from planning.extra.methods import UserSwap, getUserSwapForPlanningSwap
from planning.models import planning, availabilities, planning_swap
from mail.models import mail_adress, mail
from services.models import doctors, days, jobs, timestamps, doctors_jobs
import datetime
from datetime import timedelta

def init_db_test():
	"""	"""
	aDummyTimestamp1 = timestamps.objects.create(serial="S1", description="00h00 - 08h00")
	aDummyTimestamp2 = timestamps.objects.create(serial="S2", description="08h00 - 16h00")
	aDummyTimestamp3 = timestamps.objects.create(serial="S3", description="16h00 - 24h00")

	adays1 = days.objects.create(name = "Monday")
	adays2 = days.objects.create(name = "Tuesday")
	adays3 = days.objects.create(name = "Wenesday")
	adays4 = days.objects.create(name = "Thursday")
	adays5 = days.objects.create(name = "Friday")

	adays1.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)
	adays2.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)
	adays3.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)
	adays4.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)
	adays5.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)

	aDummyService = jobs.objects.create(name="ch_test1", serial="ch1")
	aDummyService2 = jobs.objects.create(name="ch_test2", serial="ch2")
	aDummyService3 = jobs.objects.create(name="ch_test3", serial="ch3")
	aDummyService2.linked_to.add(aDummyService)
	aDummyService.day.add(adays1,adays2,adays3,adays4,adays5)
	aDummyService2.day.add(adays1,adays2,adays3,adays4,adays5)
	aDummyService3.day.add(adays1,adays2,adays3,adays4,adays5)

	dummy1 = doctors.objects.create_user(username="kdo1", email="kdo.nguyen@gmail.com", password="toto")
	dummy2 = doctors.objects.create_user(username="kdo2", email="kdo.nguyen@gmail.com", password="toto")
	dummy3 = doctors.objects.create_user(username="kdo3", email="kdo.nguyen@gmail.com", password="toto")
	dummy4 = doctors.objects.create_user(username="kdo4", email="kdo.nguyen@gmail.com", password="toto")

	mail_adress.objects.create(muser = dummy1, email_intern="toto1@kdo.com" )
	mail_adress.objects.create(muser = dummy2, email_intern="toto2@kdo.com" )
	mail_adress.objects.create(muser = dummy3, email_intern="toto3@kdo.com" )

	doctors_jobs.objects.create(doctors=dummy1,jobs=aDummyService, status = 1)
	doctors_jobs.objects.create(doctors=dummy2,jobs=aDummyService, status = 1)
	doctors_jobs.objects.create(doctors=dummy2,jobs=aDummyService2, status = 1)
	doctors_jobs.objects.create(doctors=dummy3,jobs=aDummyService, status = 1)
	doctors_jobs.objects.create(doctors=dummy4,jobs=aDummyService, status = 0)

class planningViewTest(TestCase):

	def setUp(self):
		init_db_test()
		self.client = Client()	


	def test_simple_view_current(self):
		"""	"""
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 2, ptimestamp_id = 3)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id=  1, ptimestamp_id = 2)
		self.client.login(username='kdo1', password='toto')
		response = self.client.get('/planning/current/')
		self.assertEqual(response.status_code, 200)
		
	def test_simple_view_auto_swap(self):
		"""	"""
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 2, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id= 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id= 1, ptimestamp_id = 3)
		self.client.login(username='kdo1', password='toto')
		response = self.client.get('/planning/auto_swap/1/')
		self.assertEqual(response.status_code, 200)

	def test_simple_post_view_auto_swap(self):
		"""	"""
                planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
                planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 2, ptimestamp_id = 1)
                planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id= 1, ptimestamp_id = 2)
                planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id= 1, ptimestamp_id = 3)
		self.client.login(username='kdo1', password='toto')
		choices = [4]
		test = self.client.post('/planning/auto_swap/1/',{'subject': 'Hello du con', 
				'message':'Je vais echanger ta garde', 
				'planning_swap': choices })

		result=mail.objects.filter( cuser = doctors.objects.get(id=4))
		self.assertEqual(result[0].text, 'Je vais echanger ta garde')
		self.assertEqual(planning_swap.objects.get(id =1).planning_to_swap.id, 1)
		self.assertEqual(planning_swap.objects.get(id =1).planning_to_swap_with.id, 4)

	def test_simple_swap_request_display(self):
		"""	"""
		swap = planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 2, ptimestamp_id = 1)
		swap2 = planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id= 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id= 1, ptimestamp_id = 3)
		planning_swap.objects.create(date = datetime.date.today(), 
				planning_to_swap = swap2,
				 planning_to_swap_with = swap, 
				doctor_to_swap = doctors.objects.get(id=3),
				doctor_to_swap_with = doctors.objects.get(id=1))
		self.client.login(username='kdo1', password='toto')
		response = self.client.get('/planning/swap_request_display')
		self.assertEqual(response.status_code, 200)

	def test_simple_swap_request_accept(self):
		swap = planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 2, ptimestamp_id = 1)
		swap2 = planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id= 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id= 1, ptimestamp_id = 3)
		planning_swap.objects.create(date = datetime.date.today(),
						planning_to_swap = swap2,
						planning_to_swap_with = swap,
						doctor_to_swap = doctors.objects.get(id=3),
						doctor_to_swap_with = doctors.objects.get(id=1))
		self.client.login(username='kdo1', password='toto')
		test = self.client.post('/planning/swap_request_accept/1/')
		self.assertEqual(planning.objects.get(id=1).pdoctor.id,3)
		self.assertEqual(planning.objects.get(id=3).pdoctor.id,1)

class planningFormTest(TestCase):

	def setUp(self):
		init_db_test()

	def fill_planning_test1(self):
		"""
		"""
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 3, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id= 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id= 1, ptimestamp_id = 3)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 1) , pdoctor_id = 2, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 1) , pdoctor_id = 4, pjob_id= 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 1) , pdoctor_id = 2, pjob_id = 1, ptimestamp_id = 3)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 2) , pdoctor_id = 3, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 2) , pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 2) , pdoctor_id= 2, pjob_id = 1, ptimestamp_id = 3)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 3) , pdoctor_id= 3, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 3) , pdoctor_id= 1, pjob_id = 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today() + timedelta( days = 3) , pdoctor_id= 4, pjob_id = 1, ptimestamp_id = 3)

	def fill_planning_simple_test1(self):
		"""
			kdo1 can swap
		"""	
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 2, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id= 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id= 1, ptimestamp_id = 3)

	def fill_planning_simple_test2(self):
		"""
			kdo1 can not swap, multi services case
		"""
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 2, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id = 3, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id = 3, ptimestamp_id = 3)

	def fill_planning_simple_test3(self):
		"""
			kdo2 can swap ! multi services case
		"""
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 2, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id = 2, ptimestamp_id = 3)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id = 3, ptimestamp_id = 2)

	def test_basic_UserSwap(self):
		"""
		Test the behavior of UserSwap object
		"""
		aDummyGetUser = doctors.objects.get(username="kdo1")
		aDummySwap = UserSwap(aDummyGetUser)
		aDummySwap.setSwapInfo((datetime.date.today(),2),1)
        	self.assertEqual(aDummySwap.username,"kdo1")
		self.assertEqual(aDummySwap.email, "kdo.nguyen@gmail.com")
		self.assertEqual(aDummySwap.description, "08h00 - 16h00")
		self.assertEqual(aDummySwap.date, datetime.date.today())

	def test_basic_planning_free(self):
		"""
		Test the generation of free planning
		"""
		self.fill_planning_test1()
		self.assertEqual( [2,3,4],  
			[ int(item) 
				for item in availabilities.objects.filter(pjob_id = 1, 
									 ptimestamp_id = 2, 
									 day = datetime.date.today()
										).values_list('pdoctor_id', 
											      	flat=True )])
		self.assertEqual( [1,2,4],  
			[ int(item) 
				for item in availabilities.objects.filter(pjob_id = 1, 
									 ptimestamp_id = 3, 
									 day = datetime.date.today()
										).values_list('pdoctor_id', 
											      	flat=True )])
		self.assertEqual( [1,3,4],  
			[ int(item) 
				for item in availabilities.objects.filter(pjob_id = 1, 
									 ptimestamp_id = 1, 
									 day = datetime.date.today() + timedelta( days = 1)
										).values_list('pdoctor_id', 
												flat=True )])
		self.assertEqual( [1,2,4],  
			[ int(item) 
				for item in availabilities.objects.filter(pjob_id = 1, 
									 ptimestamp_id = 1, 
									 day = datetime.date.today() + timedelta( days = 3)
										).values_list('pdoctor_id', 
												flat=True )])
	
	def test_basic_PlanningSwapForm(self):
		"""
		Test get user for PlanningSwapForm
			user = 1
			service = 1
			day = today
			timestamp = 1
		"""
		self.fill_planning_simple_test1()
		test = PlanningSwapForm(doctor_id=1,planning_id=1)
		result = []
		result.append(
			UserSwap(doctors.objects.get(id = 3 )
				).setSwapInfo(  
					( datetime.date.today(), 3)  ,1) )
		result.append(
			UserSwap(doctors.objects.get(id = 4 )
				).setSwapInfo(  
					( datetime.date.today(), 2)  ,1) )
		
		self.assertEqual(2, len(getUserSwapForPlanningSwap(1,1)))
		self.assertEqual(result, getUserSwapForPlanningSwap(1,1))

	def test_basic_PlanningSwapForm_not_good_service1(self):
		"""
		Test get user for PlanningSwapForm no entry
			user = 2
			service = 2
			day = today
			timestamp = 1
		"""
		self.fill_planning_simple_test1()
		test = PlanningSwapForm(doctor_id=2,planning_id=2)
		self.assertEqual(0, len(getUserSwapForPlanningSwap(2,2)))

	def test_basic_PlanningSwapForm_not_multiservices(self):
		"""
		Test get user for PlanningSwapForm no entry
			user = 1
			service = 1
			day = today
			timestamp = 1
		"""
		self.fill_planning_simple_test2()
		test = PlanningSwapForm(doctor_id=1,planning_id=1)
		self.assertEqual(0, len(getUserSwapForPlanningSwap(1,1)))

	def test_basic_PlanningSwapForm_multiservices(self):
		"""
		Test get user for PlanningSwapForm
			user = 2
			service = 1
			day = today
			timestamp = 1
		"""
		self.fill_planning_simple_test3()
		test = PlanningSwapForm(doctor_id=2,planning_id=2)
		self.assertEqual(2, len(getUserSwapForPlanningSwap(2,2)))

	def test_basic_planningChangeForm_fake_planning(self):
		"""
		Test get user for PlanningSwapForm fake planning id
		"""
		self.fill_planning_simple_test1()
		test = PlanningSwapForm(doctor_id=40,planning_id=2)
		self.assertEqual(0, len(getUserSwapForPlanningSwap(40,2)))

	def test_basic_planningChangeForm_4_days(self):
		"""
		Test get user for PlanningSwapForm on 4 days
			user = 3
			service = 1
			day = today + 2
			timestamp = 1
		"""
		self.fill_planning_test1()
		test = PlanningSwapForm(doctor_id=3,planning_id=8)
		result = []
		result.append( 
			UserSwap(
				doctors.objects.get(id = 1 )
				).setSwapInfo( 
					( datetime.date.today(), 2)  ,8) )
		result.append(
			UserSwap(
				doctors.objects.get(id = 1 )
				).setSwapInfo(  
					( datetime.date.today(), 1)  ,8) )
		result.append(
			UserSwap(
				doctors.objects.get(id = 1 )
				).setSwapInfo( 
					( datetime.date.today() + timedelta( days = 3), 2 ) ,8) )
		result.append(
			UserSwap(
				doctors.objects.get(id = 1 )
				).setSwapInfo(  
					( datetime.date.today() + timedelta( days = 2), 2 ) ,8) )
		result.append(
			UserSwap(
				doctors.objects.get(id = 2 )
				).setSwapInfo(  
					( datetime.date.today() + timedelta( days = 1), 3 )  ,8) )
		result.append(
			UserSwap(
				doctors.objects.get(id = 2 )
				).setSwapInfo(
					( datetime.date.today() + timedelta( days = 2), 3 )  ,8) )
		result.append(
			UserSwap(
				doctors.objects.get(id = 2 )
				).setSwapInfo(
					( datetime.date.today() + timedelta( days = 1), 1 )  ,8) )
		result.append(
			UserSwap(
				doctors.objects.get(id = 4 )
				).setSwapInfo(
					( datetime.date.today() + timedelta( days = 1), 2 )  ,8) )
		result.append(
			UserSwap(
				doctors.objects.get(id = 4 )
				).setSwapInfo(  
					( datetime.date.today() + timedelta( days = 3), 3 )  ,8) )
		
		self.assertEqual(9, len(getUserSwapForPlanningSwap(3,8)))
		self.assertEqual(result, getUserSwapForPlanningSwap(3,8))
