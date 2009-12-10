# -*- coding: utf-8 -*-
# This file is part of Pristav.
# Copyright (c) 2009 Ionuț Arțăriși

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

from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from pristav.ads.models import Impression, Publisher, User

@login_required
def profile(request):

    cur_user = User.objects.get(username=request.user.username)
    publishers = Publisher.objects.filter(owner=cur_user)

    # build a dictionary of publisher: impressions
    pub_imp = []
    for pub in publishers:
        imp = Impression.objects.filter(publisher=pub.url).count()
        real_imp = Impression.objects.filter(referer=pub.url).count()
        pub_imp.append([pub.name, imp, real_imp])
    
    return render_to_response("profile.html", {
        'pub_imp':pub_imp},
        context_instance=RequestContext(request))
