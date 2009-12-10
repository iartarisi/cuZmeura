"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase


class ServeTests(TestCase):
    fixtures = ['mydata.json']
    def test_serve_default_publisher(self):
        response = self.client.get('/serve/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ad_url'], u'http://ceata.org/')

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

