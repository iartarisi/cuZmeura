# -*- coding: utf-8 -*-
# This file is part of cuZmeură.
# Copyright (c) 2009-2010 Ionuț Arțăriși

# cuZmeură is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# cuZmeură is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with cuZmeură.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class AdSize(models.Model):
    name = models.CharField(unique=True, max_length=20)
    size = models.CharField(unique=True, max_length=10)
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.size)

class Product(models.Model):
    name = models.CharField(unique=True, max_length=50)
    owner = models.ForeignKey(User)
    def __unicode__(self):
        return u'#%s %s belongs to: %s' % (
            self.id, self.name, self.owner.username)

class Ad(models.Model):
    name = models.CharField(unique=True, max_length=50)
    url = models.URLField()
    size = models.ForeignKey(AdSize)
    image = models.ImageField(upload_to='ads/')
    product = models.ForeignKey(Product)
    accepted = models.BooleanField(default=False)
    def __unicode__(self):
        return u'#%s %s' % (self.id, self.name)
    
class Impression(models.Model):
    ip = models.IPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    referer = models.URLField(null=True, max_length=400)
    referer_netloc = models.URLField(null=True, max_length=400)
    publisher = models.URLField()
    ad = models.ForeignKey(Ad)
    def __unicode__(self):
        return u'%s %s ref: %s' % (self.ip, self.timestamp, self.referer)

class Publisher(models.Model):
    name = models.CharField(unique=True, max_length=20)
    slug = models.SlugField(unique=True, max_length=15, editable=False)
    url = models.URLField(unique=True)
    owner = models.ForeignKey(User)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Publisher, self).save(*args, **kwargs)
    def __unicode__(self):
        return u'#%s %s | Owner: %s' % (self.id, self.name,
                                        self.owner.username)

class UserActivation(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
