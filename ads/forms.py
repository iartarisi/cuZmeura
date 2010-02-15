# -*- coding: utf-8 -*-
# This file is part of cuZmeură.
# Copyright (c) 2009-2010 Ionuț Arțăriși

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

from django import forms
from django.utils.translation import ugettext as _

from ads.models import Publisher, User

class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError(_(u"Există deja un cont cu acest nume."
                                          ))
        return unicode(username)

    def clean_password2(self):
        password = self.cleaned_data['password'] or ''
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(_(u"Cele două câmpuri pentru parolă "
                                          u"trebuie să fie identice."))
        return password2

    def save(self):
        new_user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password2'])
        new_user.is_active = False
        new_user.save()
        return new_user

class NewPublisherForm(forms.Form):
    # FIXME: test me!
    name = forms.CharField(label="Nume", max_length=20)
    slug = forms.CharField(max_length=15)
    url = forms.URLField(label="URL")
    def __init__(self, user=None, *args, **kwargs):
        super(NewPublisherForm, self).__init__(*args, **kwargs)
        self.owner = user

    def clean_name(self):
        name = self.cleaned_data['name']
        if Publisher.objects.filter(name=name):
            raise forms.ValidationError(_(
                u'Există deja un sait cu acest nume.'))
        return name

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Publisher.objects.filter(slug=slug):
            raise forms.ValidationError(_(
                u'Există deja un sait cu acest slug.'))
        return slug

    def clean_url(self):
        url = self.cleaned_data['url']
        if Publisher.objects.filter(url=url):
            raise forms.ValidationError(_(
                u'Există deja un sait cu acest url'))
        return url

    def save(self):
        new_pub = Publisher.objects.create(
            name=self.cleaned_data['name'],
            slug=self.cleaned_data['slug'],
            url=self.cleaned_data['url'],
            owner=self.owner)
        new_pub.save()
        return new_pub
