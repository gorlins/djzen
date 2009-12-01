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

