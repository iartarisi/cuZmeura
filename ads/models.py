from django.db import models

class Advertiser(models.Model):
    name = models.CharField(unique=True, max_length=50)
    url = models.URLField()
    def __unicode__(self):
        return self.name

class Ad(models.Model):
    name = models.CharField(unique=True, max_length=50)
    image = models.ImageField(upload_to='ads/')
    advertiser = models.ForeignKey(Advertiser)
    impressions = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                      editable=False)
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.impressions)

class Publisher(models.Model):
    name = models.CharField(unique=True, max_length=20)
    url = models.URLField()
    impressions = models.DecimalField(max_digits=10, decimal_places=0, default=0,
                                      editable=False)
    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.name, self.impressions)
