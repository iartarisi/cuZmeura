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

from django.db import connection, transaction
from django.http import HttpResponse
from ads.models import Ad, Impression, Product, User

import cairo
import pycha.line
from datetime import datetime

def graph_imp(request, user=None):
    '''There is a time for ugly SQL (I would love to have this rewritten)
    '''
    cursor = connection.cursor()
    cursor.execute("""
        SELECT EXTRACT(day FROM timestamp) AS days,
            COUNT(EXTRACT(day FROM timestamp))
         FROM ads_impression WHERE age(timestamp) < interval '1 month'
         GROUP BY days ORDER BY days;
         """)
    rows = cursor.fetchall()

    # # split in two months at current day
    # today = datetime.today().day
    # rows = rows[today-1:] + rows[:today-1]
    
    # fetchall returns tuples of floats for day numbers,
    # but pycha wants to iterate over ints so we do the casting ourselves
    rows = tuple(map(lambda r:(int(r[0]), int(r[1])), rows))

    # pycha datasets should look like this:
    # (('dataSet 1', ((0, 1), (1, 3), (2, 2.5))))
    dataset = tuple([tuple(['impresii', rows])])

    options = {
        'shouldFill': False,
        'colorScheme': {
            'args': {
                'initialColor': '#246673',
                },
            },
        'axis': {
            'x': {
                'label' : 'Zile',
                'tickCount': 30,
                },
            'y': {
                'label' : 'Impresii'
                }
            },
        'background' : {
            'chartColor': '#ffffff',
            'lineColor': '#FFE3EB',
            },
        'padding' : {
            'left': 50,
            },
        'legend' : {
            'hide': True,
            },

        }
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 300)
    chart = pycha.line.LineChart(surface, options)
    chart.addDataset(dataset)
    chart.render()

    # FIXME I wish cairo knew how to output to a stream
    surface.write_to_png('mytempimage.png')
    f = open('mytempimage.png')
    image = f.read()
    f.close()
    return HttpResponse(image, mimetype="image/png")
