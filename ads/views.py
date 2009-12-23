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
from urlparse import urlparse

from django.shortcuts import (render_to_response,
                              get_object_or_404, get_list_or_404)
from pristav.ads.models import Ad, Impression, Publisher

PRISTAVSLUG = 'pristav'
DEFAULT_SIZE= '125x125'

def serve(request, slugpub=None, size=DEFAULT_SIZE):
    if size == None:
        size = DEFAULT_SIZE

    # pulling all matching records isn't optimal, but it's ok at this stage
    matching_ads = get_list_or_404(Ad, size__size__exact=size)
    ad = random.choice(matching_ads)

    if request.META.has_key("HTTP_REFERER"):
        referer = request.META["HTTP_REFERER"]
        # get schema and netloc from the referer url
        referer_loc = '%s://%s' % urlparse(referer)[:2]
    else:
        referer = None
        
    if slugpub:
        publisher = get_object_or_404(Publisher, slug=slugpub)
    else:
        publisher = Publisher.objects.get(slug=PRISTAVSLUG)
        
    impression = Impression.objects.create(
        ip=request.META["REMOTE_ADDR"],
        referer = referer,
        referer_netloc = referer_loc if referer else None,
        publisher = publisher.url,
        ad = ad)
    impression.save()

    return render_to_response('serve.html', {
        'ad_url' : ad.url,
        'ad_name' : ad.name,
        'ad_img_url' : ad.image.url,
        'ad_size' : ad.size.size
        })
