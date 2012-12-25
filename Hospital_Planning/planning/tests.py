"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from planning.forms import PlanningChangeForm
from planning.models import Planning, Planning_Free
from services.models import UserHospital, Days, Services, Timestamps, Users_Services
import datetime
from datetime import timedelta
class SimpleTest(TestCase):

	def setUp(self):
		aDummyTimestamp1 = Timestamps.objects.create(serial="S1", description="Toute la journee")
		aDummyTimestamp2 = Timestamps.objects.create(serial="S2", description="1/2 journee")
		aDummyTimestamp3 = Timestamps.objects.create(serial="S3", description="Le matin")
		
		aDays1 = Days.objects.create(name = "Monday")
		aDays2 = Days.objects.create(name = "Tuesday")
		aDays3 = Days.objects.create(name = "Wenesday")
		aDays4 = Days.objects.create(name = "Thursday")
		aDays5 = Days.objects.create(name = "Friday")
		
		aDays1.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)
		aDays2.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)
		aDays3.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)
		aDays4.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)
		aDays5.timestamp.add(aDummyTimestamp1,aDummyTimestamp2,aDummyTimestamp3)

		aDummyService = Services.objects.create(name="ch_test1", serial="ch1")
		aDummyService2 = Services.objects.create(name="ch_test2", serial="ch2")
		aDummyService.day.add(aDays1,aDays2,aDays3,aDays4,aDays5)
		aDummyService2.day.add(aDays1,aDays2,aDays3,aDays4,aDays5)
		
		dummy1 = UserHospital.objects.create(username="kdo1", email="kdo.nguyen@gmail.com", password="toto")
		dummy2 = UserHospital.objects.create(username="kdo2", email="kdo.nguyen@gmail.com", password="toto")
		dummy3 = UserHospital.objects.create(username="kdo3", email="kdo.nguyen@gmail.com", password="toto")
		dummy4 = UserHospital.objects.create(username="kdo4", email="kdo.nguyen@gmail.com", password="toto")

		Users_Services.objects.create(users=dummy1,services=aDummyService, status = 1)
		Users_Services.objects.create(users=dummy2,services=aDummyService, status = 1)
		Users_Services.objects.create(users=dummy2,services=aDummyService2, status = 1)
		Users_Services.objects.create(users=dummy3,services=aDummyService, status = 1)
		Users_Services.objects.create(users=dummy4,services=aDummyService, status = 0)

	def fill_planning_test1(self):
		Planning.objects.create(day = datetime.date.today(), puser_id = 1, pservice_id = 1, ptimestamp_id = 1)
		Planning.objects.create(day = datetime.date.today(), puser_id = 1, pservice_id= 1, ptimestamp_id = 2)
		Planning.objects.create(day = datetime.date.today(), puser_id = 3, pservice_id= 1, ptimestamp_id = 3)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 1) , puser_id = 2, pservice_id = 1, ptimestamp_id = 1)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 1) , puser_id = 4, pservice_id= 1, ptimestamp_id = 2)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 1) , puser_id = 2, pservice_id = 1, ptimestamp_id = 3)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 2) , puser_id = 3, pservice_id = 1, ptimestamp_id = 1)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 2) , puser_id = 1, pservice_id = 1, ptimestamp_id = 2)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 2) , puser_id= 2, pservice_id = 1, ptimestamp_id = 3)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 3) , puser_id= 3, pservice_id = 1, ptimestamp_id = 1)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 3) , puser_id= 1, pservice_id = 1, ptimestamp_id = 2)
		Planning.objects.create(day = datetime.date.today() + timedelta( days = 3) , puser_id= 4, pservice_id = 1, ptimestamp_id = 3)

 	

	def test_basic_UserSwap(self):
		"""
		Test the behavior of UserHospitalSwap object
		"""
		aDummyGetUser = UserHospital.objects.get(username="kdo1")
		aDummySwap = PlanningChangeForm.UserSwap(aDummyGetUser)
		aDummySwap.date([(datetime.date.today(),2)])
        	self.assertEqual(aDummySwap.username,"kdo1")
		self.assertEqual(aDummySwap.email, "kdo.nguyen@gmail.com")
		self.assertEqual(aDummySwap.description, "1/2 journee")
		self.assertEqual(aDummySwap.date, datetime.date.today())

	def test_planning_free(self):
		self.fill_planning_test1()
		self.assertEqual( [long(2),long(3),long(4)], Planning_Free.objects.filter(pservice_id = 1, ptimestamp_id = 1, day = datetime.date.today()).values_list('puser_id', flat=True))
	
