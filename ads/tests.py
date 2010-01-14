# -*- coding: utf-8 -*-
# This file is part of Pristav.
# Copyright (c) 2009-2010 Ionuț Arțăriși

# Chematoru' is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# Pristav is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Pristav.  If not, see <http://www.gnu.org/licenses/>.

from django.test import TestCase
from pristav.ads.models import Impression, Ad

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

    def test_serve_notexists_publisher(self):
        response = self.client.get('/serve/notfound')
        self.assertEqual(response.status_code, 404)

    def test_serve_size_match_regex(self):
        response = self.client.get('/serve/pristav/')
        self.assertEqual(response.context['ad_size'], '125x125')
        
        response = self.client.get('/serve/pristav/125x125')
        self.assertEqual(response.context['ad_size'], '125x125')

    def test_serve_size_not_found(self):
        response = self.client.get('/serve/pristav/0x0')
        self.assertEqual(response.status_code, 404)

    def test_serve_size_mismatch_regex(self):
        invalid_url = ['/serve/x125',
                        '/serve/x125',
                        '/serve/x12y',
                        '/serve/125x',
                        '/serve/12yx',
                        '/serve/125x1y',
                        '/serve/12yx125',
                        '/serve/y']
        for res in invalid_url:
            response = self.client.get(res)
            self.assertEqual(response.status_code, 404)

    def test_serve_correct_referer_netloc(self):
        response = self.client.get('/serve/pristav/125x125',
                                   HTTP_REFERER='http://pristav.ceata.org/xmpl')
        impre = Impression.objects.all()[0]
        self.assertEqual(impre.referer, 'http://pristav.ceata.org/xmpl')
        self.assertEqual(impre.referer_netloc, 'http://pristav.ceata.org/')
        # clean up
        Impression.objects.all()[0].delete()

    def test_ads_sequentiality(self):
        for j in range(3): # go three times through every ad in the db
            for i in range(3):
                response = self.client.get('/serve/pristav/125x125')
                self.assertEqual(response.context['ad_name'],
                                 Ad.objects.all()[i].name)
