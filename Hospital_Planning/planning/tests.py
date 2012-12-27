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

		aDummyTimestamp1 = Timestamps.objects.create(serial="S1", description="00h00 - 08h00")
		aDummyTimestamp2 = Timestamps.objects.create(serial="S2", description="08h00 - 16h00")
		aDummyTimestamp3 = Timestamps.objects.create(serial="S3", description="16h00 - 24h00")
		
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
		aDummyService3 = Services.objects.create(name="ch_test3", serial="ch3")
		aDummyService2.linked_to.add(aDummyService)
		aDummyService.day.add(aDays1,aDays2,aDays3,aDays4,aDays5)
		aDummyService2.day.add(aDays1,aDays2,aDays3,aDays4,aDays5)
		aDummyService3.day.add(aDays1,aDays2,aDays3,aDays4,aDays5)
		
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
		"""
		"""
		Planning.objects.create(day = datetime.date.today(), puser_id = 1, pservice_id = 1, ptimestamp_id = 1)
		Planning.objects.create(day = datetime.date.today(), puser_id = 2, pservice_id = 3, ptimestamp_id = 1)
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

	def fill_planning_simple_test1(self):
		Planning.objects.create(day = datetime.date.today(), puser_id = 1, pservice_id = 1, ptimestamp_id = 1)
		Planning.objects.create(day = datetime.date.today(), puser_id = 2, pservice_id = 2, ptimestamp_id = 1)
		Planning.objects.create(day = datetime.date.today(), puser_id = 4, pservice_id= 1, ptimestamp_id = 2)
		Planning.objects.create(day = datetime.date.today(), puser_id = 3, pservice_id= 1, ptimestamp_id = 3)

	def test_basic_UserSwap(self):
		"""
		Test the behavior of UserSwap object
		"""
		aDummyGetUser = UserHospital.objects.get(username="kdo1")
		aDummySwap = PlanningChangeForm.UserSwap(aDummyGetUser)
		aDummySwap.date((datetime.date.today(),2))
        	self.assertEqual(aDummySwap.username,"kdo1")
		self.assertEqual(aDummySwap.email, "kdo.nguyen@gmail.com")
		self.assertEqual(aDummySwap.description, "08h00 - 16h00")
		self.assertEqual(aDummySwap.date, datetime.date.today())

	def test_basic_planning_free(self):
		"""
		Test the generation of free planning
		"""
		self.fill_planning_test1()
		self.assertEqual( [2,3,4],  [int(item) for item in Planning_Free.objects.filter(pservice_id = 1, ptimestamp_id = 2, day = datetime.date.today()).values_list('puser_id', flat=True)])
		self.assertEqual( [1,2,4],  [int(item) for item in Planning_Free.objects.filter(pservice_id = 1, ptimestamp_id = 3, day = datetime.date.today()).values_list('puser_id', flat=True)])
		self.assertEqual( [1,3,4],  [int(item) for item in Planning_Free.objects.filter(pservice_id = 1, ptimestamp_id = 1, day = datetime.date.today() + timedelta( days = 1)).values_list('puser_id', flat=True)])
		self.assertEqual( [1,2,4],  [int(item) for item in Planning_Free.objects.filter(pservice_id = 1, ptimestamp_id = 1, day = datetime.date.today() + timedelta( days = 3)).values_list('puser_id', flat=True)])
	
	def test_basic_PlanningChangeForm(self):
		"""
		Test get user for planningChangeForm
		"""
		self.fill_planning_simple_test1()
		test = PlanningChangeForm(user_id=1, service_id='1', timestamp_id='1',day=datetime.date.today() )
		result = []
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 3 )).date(  (datetime.date.today(), 3)  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 4 )).date(  (datetime.date.today(), 2)  ) )
		self.assertEqual(2, len(test.fields['users'].choices))
		self.assertEqual(result, test.fields['users'].choices)

	def test_basic_PlanningChangeForm_not_good_service(self):
		"""
		Test get user for planningChangeForm no entry
		"""
		self.fill_planning_simple_test1()
		test = PlanningChangeForm(user_id=2, service_id='2', timestamp_id='1',day=datetime.date.today() )
		self.assertEqual(0, len(test.fields['users'].choices))

	def test_basic_PlanningChangeForm_fake_planning(self):
		"""
		Test get user for planningChangeForm fake user
		"""
		self.fill_planning_simple_test1()
		test = PlanningChangeForm(user_id=5, service_id='2', timestamp_id='1',day=datetime.date.today() )
		self.assertEqual(0, len(test.fields['users'].choices))

	def test_basic_PlanningChangeForm_4_days(self):
		"""
		Test get user for planningChangeForm on 4 days
		"""
		self.fill_planning_test1()
		test = PlanningChangeForm(user_id=3, service_id='1', timestamp_id='1',day=datetime.date.today() + timedelta( days = 2) )
		result = []
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 1 )).date(  (datetime.date.today(), 2)  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 1 )).date(  (datetime.date.today(), 1)  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 1 )).date(  (datetime.date.today() + timedelta( days = 3), 2 )  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 1 )).date(  (datetime.date.today() + timedelta( days = 2), 2 )  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 2 )).date(  (datetime.date.today() + timedelta( days = 1), 3 )  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 2 )).date(  (datetime.date.today() + timedelta( days = 2), 3 )  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 2 )).date(  (datetime.date.today() + timedelta( days = 1), 1 )  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 4 )).date(  (datetime.date.today() + timedelta( days = 1), 2 )  ) )
		result.append(PlanningChangeForm.UserSwap(UserHospital.objects.get(id = 4 )).date(  (datetime.date.today() + timedelta( days = 3), 3 )  ) )
		self.assertEqual(9, len(test.fields['users'].choices))
		self.assertEqual(result, test.fields['users'].choices)
#		for i in test.fields['users'].choices:
#			print i

