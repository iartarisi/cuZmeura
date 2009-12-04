import random

from django.shortcuts import render_to_response, HttpResponse
from chematoru.ads.models import Ad, Publisher

def serve(self, pubid, size='125x125'):
    publisher = Publisher.objects.get(id=pubid)
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

def index(self):
    return render_to_response('index.html', {
        'domain': "http://chematoru.ceata.org"})

