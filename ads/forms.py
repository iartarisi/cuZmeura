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

from ads.models import User

class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError(_("An account with this username has "
                                        "already been created."))
        return username
        
    def clean_password2(self):
        password = self.cleaned_data['password'] or ''
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(_("The two password fields must be the "
                                        "same."))
        return password2
        
    def save(self):
        new_user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password2'])
        new_user.is_active = False
        new_user.save()
        return new_user
        

