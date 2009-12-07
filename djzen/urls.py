"""URLs"""
"""
    Copyright 2009 Scott Gorlin

    This file is part of Djzen.

    Djzen is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Djzen is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Djzen.  If not, see <http://www.gnu.org/licenses/>.
"""
#from django.conf import settings
from django.conf.urls.defaults import *
from models import *


urlpatterns = patterns('djzen.views', #'django.views.generic.list_detail',
                       
                       url(r'^$',
                           'renderGroup',
                           {'object_id':User.objects.all()[0].RootGroup.Id},
                           name='djzen-galleryRoot'),
                       
                       #url(r'^$', 'object_detail', 
                           #{'queryset': Group.objects.all(),
                            #'object_id': User.objects.all()[0].RootGroup.Id},
                           #name='djzen-galleryRoot'),
                       
                       url(r'^f(?P<object_id>\d+)/$',
                           'renderGroup', 
                           {}, 
                           name='djzen-group'),
                       
                       #url(r'^f(?P<object_id>\d+)/$', 'object_detail', 
                           #{'queryset': Group.objects.all()}, 
                           #name='djzen-group'),
                       
                       url(r'^p(?P<object_id>\d+)/$', 'renderPhotoSet', 
                           {'queryset': PhotoSet.objects.all()},
                           name='djzen-photoset'),
                       url(r'^photo(?P<object_id>\d+)/$', 'renderPhoto',
                           {'queryset': Photo.objects.all()},
                           name='djzen-photo'),
                       )

