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

from django.db import models

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

class Ad(models.Model):
    name = models.CharField(unique=True, max_length=50)
    url = models.URLField()
    image = models.ImageField(upload_to='ads/')
    advertiser = models.ForeignKey(Advertiser)
    size = models.ForeignKey(AdSize)
    impressions = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                      editable=False)
    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.name, self.impressions)

class Publisher(models.Model):
    name = models.CharField(unique=True, max_length=20)
    url = models.URLField()
    impressions = models.DecimalField(max_digits=10, decimal_places=0, default=0,
                                      editable=False)
    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.name, self.impressions)

