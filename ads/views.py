from random import randint

from django.shortcuts import render_to_response, HttpResponse
from chematoru.ads.models import Ad, Publisher

def serve(self, pubid):
    publisher = Publisher.objects.get(id=pubid)
    publisher.impressions += 1
    publisher.save()
    
    ads_count = Ad.objects.count()
    ad = Ad.objects.get(id= randint(1, ads_count))
    
    ad.impressions += 1
    ad.save()
    return render_to_response('serve.html', {
        'publisher_url' : ad.advertiser.url,
        'ad_name' : ad.name,
        'ad_url' : ad.image.url})

def index(self):
    return render_to_response('index.html', {
        'domain': "http://chematoru.ceata.org"})

