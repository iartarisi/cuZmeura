# -*- coding: utf-8 -*-
# This file is part of Pristav.
# Copyright (c) 2009 Ionuț Arțăriși

# Pristav is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# Pristav is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Pristav.  If not, see <http://www.gnu.org/licenses/>.

import random

from django.shortcuts import render_to_response, HttpResponse
from pristav.ads.models import Ad, Impression, Publisher

PRISTAVSLUG = 'pristav'
def serve(request, slugpub=None, size='125x125'):
    # pulling all matching records isn't optimal, but it's ok at this stage
    matching_ads = Ad.objects.filter(size__size__exact=size)
    ad = random.choice(matching_ads)

    if request.META.has_key("HTTP_REFERER"):
        referer = request.META["HTTP_REFERER"]
    else:
        referer = None
        
    if slugpub:
        publisher = Publisher.objects.get(slug=slugpub)
    else:
        publisher = Publisher.objects.get(slug=PRISTAVSLUG)
        
    impression = Impression.objects.create(ip=request.META["REMOTE_ADDR"],
                                           referer = referer,
                                           publisher = publisher.url,
                                           ad = ad)
    impression.save()

    return render_to_response('serve.html', {
        'ad_url' : ad.url,
        'ad_name' : ad.name,
        'ad_img_url' : ad.image.url})
