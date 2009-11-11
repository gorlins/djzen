#from django.conf import settings
from django.conf.urls.defaults import *
from models import *


urlpatterns = patterns('django.views.generic.list_detail',
                       url(r'^$', 'object_detail', 
                           {'queryset': Group.objects.all(),
                            'object_id': User.objects.all()[0].RootGroup.Id},
                           name='djzen-galleryRoot'),
                       url(r'^f(?P<object_id>\d+)/$', 'object_detail', 
                           {'queryset': Group.objects.all()}, 
                           name='djzen-group'),
                       url(r'^p(?P<object_id>\d+)/$', 'object_detail', 
                           {'queryset': PhotoSet.objects.all()},
                           name='djzen-photoset'),
                       url(r'^photo(?P<object_id>\d+)/$', 'object_detail',
                           {'queryset': Photo.objects.all()},
                           name='djzen-photo'),
                       )

