# -*- coding: utf-8 -*-
# This file is part of cuZmeură.
# Copyright (c) 2010 Ionuț Arțăriși

# cuZmeură is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# cuZmeură is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with cuZmeură.  If not, see <http://www.gnu.org/licenses/>.

from django.test import TestCase

class PublisherFormTests(TestCase):
    fixtures = ['one_good_user']
    username = 'gigel'
    password = 'gigipass'
    
    def test_two_names_same_slug(self):
        '''Two different names that generate the same slug must fail
        '''
        post_data1 = {
            'name': 'Foo Bâr#$*',
            'url': 'http://example.com'
            }
        post_data2 = {
            'name': 'FOO BAR',
            'url': 'http://example.com'
            }
        login = self.client.login(username=self.username,
                                  password=self.password)
        response = self.client.post('/user/profile/', post_data1)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/user/profile/', post_data2)
        self.assertFormError(response, 'form', 'name',
                             u'Există deja un sait cu acest nume.')

            
        
