"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from planning.forms import PlanningSwapForm
from planning.extra.methods import UserSwap, getUserSwapForPlanningSwap, handle_uploaded_planning
from planning.models import planning, planning_swap
from planning.models import doctors, days, jobs, timestamps#, doctors_jobs
import datetime, os, csv
from datetime import timedelta

def init_db_test():
	"""	"""
	aDummyTimestamp1 = timestamps.objects.create(serial="am", description="00h00 - 08h00")
	aDummyTimestamp2 = timestamps.objects.create(serial="m", description="08h00 - 16h00")
	aDummyTimestamp3 = timestamps.objects.create(serial="n", description="16h00 - 24h00")

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

	dummy1.djobs.add(aDummyService)
	dummy2.djobs.add(aDummyService,aDummyService2)
	dummy3.djobs.add(aDummyService)
	dummy4.djobs.add(aDummyService)

class planningViewTest(TestCase):

	def setUp(self):
		init_db_test()
		self.client = Client()	
		
	def test_simple_view_auto_swap(self):
		"""	"""
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 2, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id= 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id= 1, ptimestamp_id = 3)
		self.client.login(username='kdo1', password='toto')
		response = self.client.get('/planning/auto_swap_request/1/')
		self.assertEqual(response.status_code, 200)

	def test_simple_view_import(self):
		"""	"""
		self.client.login(username='kdo1', password='toto')
		response = self.client.get('/planning/import_planning/')
		self.assertEqual(response.status_code, 200)

	def test_simple_post_view_auto_swap(self):
		"""	"""
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 1, pjob_id = 1, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 2, pjob_id = 2, ptimestamp_id = 1)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 4, pjob_id= 1, ptimestamp_id = 2)
		planning.objects.create(day = datetime.date.today(), pdoctor_id = 3, pjob_id= 1, ptimestamp_id = 3)
		self.client.login(username='kdo1', password='toto')
		choices = [4]
		test = self.client.post('/planning/auto_swap_request/1/',{'subject': 'Hello du con', 
				'message':'Je vais echanger ta garde', 
				'planning_swap': choices })

		#result=mail.objects.filter( cuser = doctors.objects.get(id=4))
		#self.assertEqual(result[0].text, 'Je vais echanger ta garde')
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
		test = self.client.post('/planning/accept_swap/1/')
		#self.assertEqual(planning.objects.get(id=1).pdoctor.id,3)
		#self.assertEqual(planning.objects.get(id=3).pdoctor.id,1)
