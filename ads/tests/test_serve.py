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
from pristav.ads.models import Impression, Ad, Product

class ServeTests(TestCase):
    fixtures = ['ads.json']

    def _test_get_publisher(self, puburl):
        """
        Test for default publisher.
        """
        response = self.client.get('/serve/' + puburl)

        # get the ads belonging to the first Product
        ads = [a.name for a in Product.objects.all()[0].ad_set.all()]
        
        self.assertEqual(response.status_code, 200)
        self.assert_(response.context['ad_name'] in ads)

    def test_no_publisher(self):
        self._test_get_publisher('')
        
    def test_pristav_publisher(self):
        self._test_get_publisher('default')

    def test_notexists_publisher(self):
        response = self.client.get('/serve/notfound')
        self.assertEqual(response.status_code, 404)

    def test_size_match_regex(self):
        response = self.client.get('/serve/default/')
        self.assertEqual(response.context['ad_size'], '125x125')
        
        response = self.client.get('/serve/default/125x125')
        self.assertEqual(response.context['ad_size'], '125x125')

    def test_size_not_found(self):
        response = self.client.get('/serve/default/0x0')
        self.assertEqual(response.status_code, 404)

    def test_size_mismatch_regex(self):
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

    def test_correct_referer_netloc(self):
        response = self.client.get('/serve/default/125x125',
                                   HTTP_REFERER='http://pristav.ceata.org/xmpl')
        impre = Impression.objects.all()[0]
        self.assertEqual(impre.referer, 'http://pristav.ceata.org/xmpl')
        self.assertEqual(impre.referer_netloc, 'http://pristav.ceata.org/')
        # clean up
        Impression.objects.all()[0].delete()

    def test_ads_sequentiality(self):
        '''Serve ads from each product sequentially
        '''

        ads1 = Product.objects.all()[0].ad_set.all()
        ads2 = Product.objects.all()[1].ad_set.all()

        ads = [[a.name for a in ads] for ads in [ads1, ads2]]

        for req in [0,1,0,1]:
            response = self.client.get('/serve/default/125x125')
            self.assert_(response.context['ad_name'] in ads[req])
    def test_no_unaccepted_ads(self):
        '''Unaccepted ads never get shown
        '''
        bogus = Ad.objects.filter(accepted=False).all()[0]
        for req in range(10):
            response = self.client.get('/serve/default/')
            self.assertNotEquals(bogus.name, response.context['ad_name'])
