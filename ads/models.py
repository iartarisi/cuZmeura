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

from django.db import models
from django.contrib.auth.models import User

class Advertiser(models.Model):
    name = models.CharField(unique=True, max_length=50)
    url = models.URLField()
    def __unicode__(self):
        return self.name

class AdSize(models.Model):
    name = models.CharField(unique=True, max_length=20)
    size = models.CharField(unique=True, max_length=10)
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.size)

class Product(models.Model):
    name = models.CharField(unique=True, max_length=50)
    advertiser = models.ForeignKey(Advertiser)
    def __unicode__(self):
        return u'#%s %s' % (self.id, self.name)

class Ad(models.Model):
    name = models.CharField(unique=True, max_length=50)
    url = models.URLField()
    size = models.ForeignKey(AdSize)
    image = models.ImageField(upload_to='ads/')
    product = models.ForeignKey(Product)
    def __unicode__(self):
        return u'#%s %s' % (self.id, self.name)

    
class Impression(models.Model):
    ip = models.IPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    referer = models.URLField(null=True)
    referer_netloc = models.URLField(null=True)
    publisher = models.URLField()
    ad = models.ForeignKey(Ad)
    def __unicode__(self):
        return u'%s %s ref: %s' % (self.ip, self.timestamp, self.referer)

class Publisher(models.Model):
    name = models.CharField(unique=True, max_length=20)
    slug = models.SlugField(unique=True, max_length=10)
    url = models.URLField()
    owner = models.ForeignKey(User)
    def __unicode__(self):
        return u'#%s %s | Owner: %s' % (self.id, self.name,
                                        self.owner.username)

