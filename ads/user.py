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

import datetime, hashlib, random

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from ads.forms import UserRegistrationForm
from ads.models import Impression, Publisher, User, UserActivation

# FIXME: use contrib.sites perhaps?
# also check out the hardcoding in urls.py
PRISTAVURL = 'http://pristav.ceata.org/'
PRISTAVEMAIL = 'pristav@ceata.org'
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            # Build the activation key
            salt = hashlib.md5(str(random.random())).hexdigest()[-5:]
            activation_key = hashlib.md5(salt+new_user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            new_activ = UserActivation(user=new_user,
                                       activation_key=activation_key,
                                       key_expires=key_expires)
            new_activ.save()

            # FIXME: move this to a template?
            # Send email with the activation information
            email_subject = _("Your Pristav account activation")
            email_body = _("Hello %s, \n"
                           "Thanks for signing up for the Pristav advertising "
                           "network.\n"
                           "You can activate your account by following this "
                           "link in the next 2 days: %s" % (
                               new_user.username,
                               PRISTAVURL+'confirm/'+activation_key))
            send_mail(email_subject, email_body, PRISTAVEMAIL,
                      [new_user.email])

            return redirect("/user/profile/")
    else:
        form = UserRegistrationForm()
    return render_to_response("register.html", {
        'form': form})

def confirm(request, activation_key):
    if request.user.is_authenticated():
        return redirect("/user/profile/")
    user_activ = get_object_or_404(UserActivation,
                                   activation_key=activation_key)
    if user_activ.key_expires < datetime.datetime.today():
        return render_to_response("confirm.html", {"expired":True})

    user = user_activ.user
    user.is_active = True
    user.save()
    return render_to_response("confirm.html", {'success':True})
    
@login_required
def profile(request):
    cur_user = User.objects.get(username=request.user.username)
    publishers = Publisher.objects.filter(owner=cur_user)

    # list of [publisher_url, impression, real_impression]
    pub_imp = []
    for pub in publishers:
        imp = Impression.objects.filter(publisher=pub.url).count()
        real_imp = Impression.objects.filter(referer_netloc=pub.url).count()
        pub_imp.append([pub.name, pub.slug, imp, real_imp])
    
    return render_to_response("profile.html", {
        'pub_imp':pub_imp,
        'domain': PRISTAVURL,
        },
        context_instance=RequestContext(request))
