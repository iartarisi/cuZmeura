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

import datetime

from django.core import mail
from django.test import TestCase

from ads.models import User, UserActivation
from ads.forms import UserRegistrationForm

class RegistrationTests(TestCase):
    good_data = {
        'username':'gigi',
        'email': 'gigi@gigi.gi',
        'password': 'gigipass',
        'password2': 'gigipass'
        }
    def test_get_registration_form(self):
        '''GET the registration form
        '''
        response = self.client.get('/user/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_empty_registration_post(self):
        '''POST an empty dictionary to the registration form
        '''
        response = self.client.post('/user/register/', {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        required = 'This field is required.'
        self.assertFormError(response,'form','email', required)
        self.assertFormError(response, 'form', 'username', required)
        self.assertFormError(response, 'form', 'password', required)
        self.assertFormError(response, 'form', 'password2', required)
        
    def test_post_correct_form(self):
        '''POST correct data to registration form

        Verify that the email is sent and the thank you message is displayed.
        '''
        response = self.client.post('/user/register/', self.good_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertTrue(response.context['thanks'])
        self.assertEquals(len(mail.outbox), 1)
        self.failUnless('gigi' in mail.outbox[0].body)

    def test_differing_passwords(self):
        '''POST differing passwords to registration form'''
        post_data = {
            'username': 'gigi',
            'email': 'gigi@example.com',
            'password': 'gigi',
            'password2': 'NOTgigi'
            }

        response = self.client.post('/user/register/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'password2',
                             "The two password fields must be the same.")

    def test_user_exists(self):
        '''POST two users with the same name

        make two requests, we do not bother with the first one,
        it should have been tested elsewhere
        '''
        self.client.post('/user/register/', self.good_data)
        response = self.client.post('/user/register/', self.good_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'username',
                             'An account with this username has already been '
                             'created.')
                             
    def test_activate_with_key(self):
        '''POST good data and use validation key to confirm'''
        self.client.post('/user/register/', self.good_data)

        ua = UserActivation.objects.get(pk=1)
        self.assertFalse(ua.user.is_active)

        response = self.client.get('/user/confirm/%s' % ua.activation_key)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confirm.html")
        self.assertTrue(response.context['success'])

        # reget to refresh the cache
        ua = UserActivation.objects.get(pk=1)
        self.assertTrue(ua.user.is_active)

        # second time, it should already be active
        response = self.client.get('/user/confirm/%s' % ua.activation_key)
        self.assertTemplateUsed(response, "confirm.html")
        self.assertTrue(response.context["already_active"])

    def test_bad_activation(self):
        '''GET with a bad activation key'''
        response = self.client.get('/user/confirm/THIS_IS_NO_MD5')
        self.assertEqual(response.status_code, 404)

    def test_user_login_without_activation(self):
        '''Users cannot login without activation'''
        self.client.post('/user/register/', self.good_data)

        login = self.client.login(username=self.good_data['username'],
                                  password=self.good_data['password'])
        self.failIf(login)
        
    def test_expired_activation_key(self):
        '''Activation key should expire in 2 days'''
        self.client.post('/user/register/', self.good_data)

        ua = UserActivation.objects.get(pk=1)

        # key expires somewhere between tomorow and the day after tomorow
        self.assert_(datetime.timedelta(1) <
                     (ua.key_expires - datetime.datetime.today()))
        self.assert_(datetime.timedelta(2) >
                     (ua.key_expires - datetime.datetime.today()))

        # expire it now and see what happens
        ua.key_expires = datetime.datetime.now()
        ua.save()

        response = self.client.get('/user/confirm/%s' % ua.activation_key)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['expired'])
        self.assertTemplateUsed(response, 'confirm.html')

    def test_user_is_authenticated(self):
        '''Authenticated users should be redirected to their profile page
        '''
        self.client.post('/user/register/', self.good_data)

        # activate account before logging in
        ua = UserActivation.objects.get(pk=1)
        ua.user.is_active = True
        ua.user.save()
        
        login = self.client.login(username=self.good_data['username'],
                                  password=self.good_data['password'])
        self.assertTrue(login)
        
        response = self.client.get('/user/confirm/%s' % ua.activation_key)
        self.assertRedirects(response, '/user/profile/')
