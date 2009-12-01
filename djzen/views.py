# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
import operator
from models import *

def renderGroup(request, object_id=None):
    """Prepares a group for display
    
    In addition to sending the group object directly to the template, this view:
    
    Flattens any child group with FlattenMe=True by pulling out the photosets
    for display here.  This is very useful for groups with a single contained
    photoset of the same name as the group
    """
    
    group = get_object_or_404(Group, Id=object_id)
    
    groupChildren = group.GroupElements.exclude(FlattenMe=True)
    
    newPSChildren = [g.PhotoSetElements.all() for g in \
                     group.GroupElements.filter(FlattenMe=True)]
    
    photosetChildren = reduce(operator.or_, newPSChildren,
                              group.PhotoSetElements.all())
    
    return render_to_response('djzen/group_detail.html', 
                              {'object':group, 
                               'groupChildren':groupChildren, 
                               'photosetChildren':photosetChildren, 
                               'request':request})

def renderPhoto(request, object_id=None):
    photo = get_object_or_404(Photo, Id=object_id)
    return render_to_response('djzen/photo_detail.html',
                              {'object':photo,
                               'request':request})

def renderPhotoSet(request, object_id=None):
    ps = get_object_or_404(Group, Id=object_id)
    return render_to_response('djzen/photoset_detail.html',
                              {'object':ps,
                               'request':request})
