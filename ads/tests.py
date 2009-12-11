"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase


class ServeTests(TestCase):
    fixtures = ['mydata.json']
    
     
    def _test_serve_default_publisher(self, puburl):
        """
        Test for default publisher.
        """
        response = self.client.get('/serve/' + puburl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ad_url'], u'http://ceata.org/')
        self.assertEqual(response.context['ad_name'], u'Ceata')
        self.assertEqual(response.context['ad_img_url'],
                         u'http://localhost:8000/media/ads/ceata_.png')

    def test_serve_default_publisher(self):
        self._test_serve_default_publisher('')
        
    def test_serve_pristav_publisher(self):
        self._test_serve_default_publisher('pristav')
