"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from calandars.models import Timestamps, Days, Calandars

class SimpleTest(TestCase):
    def test_simple_calandars(self):
        """
        Tests Calandars models
        """
	aTimer1 = Timestamps.objects.create(serial="S1", start="0900", stop="1800")
	aTimer2 = Timestamps.objects.create(serial="S2", start="1900", stop="0000")
	aDays1 = Days.objects.create(day=1, name="Monday")
	aDays2 = Days.objects.create(day=2, name="Tuesday")
	aDays3 = Days.objects.create(day=3, name="Wenesday")
	aDays4 = Days.objects.create(day=4, name="Thursday")
	aDays5 = Days.objects.create(day=5, name="Friday")
	aDays1.timestamp.add(aTimer1, aTimer1)
	aDays2.timestamp.add(aTimer1, aTimer1)
	aDays3.timestamp.add(aTimer1, aTimer1)
	aDays4.timestamp.add(aTimer1, aTimer1)
	aDays5.timestamp.add(aTimer1, aTimer1)
	aCalandar = Calandars.objects.create(service="CHS Le Mans", serial="CHSPSY")
	aCalandar.day.add(aDays1,aDays2,aDays3,aDays4,aDays5)
	aCalandar.save()
	
	aCalandarFromDb = Calandars.objects.get(service="CHS Le Mans")
	self.assertEqual(aCalandarFromDb.service, "CHS Le Mans")
	self.assertEqual(aCalandarFromDb.serial, "CHSPSY")
	self.assertEqual(aCalandarFromDb.day.all()[0].name, "Monday")
	self.assertEqual(aCalandarFromDb.day.all()[1].name, "Tuesday")
	self.assertEqual(aCalandarFromDb.day.all()[2].name, "Wenesday")
	self.assertEqual(aCalandarFromDb.day.all()[3].name, "Thursday")
	self.assertEqual(aCalandarFromDb.day.all()[4].name, "Friday") 
