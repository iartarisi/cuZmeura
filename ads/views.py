# -*- coding: utf-8 -*-
# This file is part of Chemătoru'.
# Copyright (c) 2009 Ionuț Arțăriși

# Chematoru' is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# Chemătoru' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Chemătoru'.  If not, see <http://www.gnu.org/licenses/>.

import random

from django.shortcuts import render_to_response, HttpResponse
from chematoru.ads.models import Ad, Publisher

def serve(request, slugpub=None, size='125x125'):
    if slugpub:
        publisher = Publisher.objects.get(slug=slugpub)
    else:
        publisher = Publisher.objects.all()[0]
    publisher.impressions += 1
    publisher.save()

    # pulling all matching records isn't optimal, but it's ok at this stage
    matching_ads = Ad.objects.filter(size__size__exact=size)
    ad = random.choice(matching_ads)

    ad.impressions += 1
    ad.save()
    return render_to_response('serve.html', {
        'ad_url' : ad.url,
        'ad_name' : ad.name,
        'ad_img_url' : ad.image.url})

def index(request):
    return render_to_response('index.html', {
        'domain': request.build_absolute_uri('/')})
