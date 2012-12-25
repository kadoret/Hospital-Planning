"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from services.models import Timestamps, Days, Services

class SimpleTest(TestCase):
    def test_simple_services(self):
        """
        Tests services beahvior
        """
