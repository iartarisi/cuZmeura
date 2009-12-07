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

from pristav.ads.models import Impression, Publisher

@login_required
def profile(request):
    pub = Publisher.objects.get()
    impressions = Impression.objects.filter(
        referer='http://localhost:8000/').count()

    return render_to_response("profile.html", {
        'impressions':impressions},
                              context_instance=RequestContext(request))

    
    
    
    

