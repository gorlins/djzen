"""Template tags"""
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

from django import template
import os
from django.template.defaultfilters import slugify

register = template.Library()


#def thumbstr(im, thumb):
    #return '<a title="%s" href="%s"><img src="%s" width=%dpx height=%dpx/></a>' % (im.Title, im.get_absolute_url(), thumb.url, thumb.width, thumb.height)

#@register.simple_tag
#def thumbnail(im):
    #if im.is_public: thumb = im.thumbnail
    #else: thumb = im.privatethumbnail
    #return thumbstr(im, thumb)


#@register.simple_tag
#def smallthumb(im):
    #if im.is_public: thumb = im.smallthumb
    #else: thumb = im.privatesmallthumb
    #return thumbstr(im, thumb)
    
#@register.simple_tag
#def textlink(folder):
    #if not folder.is_public:
        #mid = '<i>%s</i>'%folder.title
    #else:
        #mid = '%s'%folder.title

    #return '<a title="%s" href="%s">%s</a>' % (folder.title, folder.get_absolute_url(), mid)
    
#@register.simple_tag
#def next_n_in_gallery(photo, gallery, n):
    #out = []
    #next = photo
    #while next and n > 0:
        #next=next.get_next_in_gallery(gallery)
        #out.append(next)
        #n-=1
    #return out

#@register.simple_tag
#def previous_n_in_gallery(photo, gallery, n):
    #out = []
    #prev=photo
    #while prev and n > 0:
        #prev=prev.get_previous_in_gallery(gallery)
        #out.append(prev)
        #n-=1
    #out.reverse()
    #return out

#@register.filter
#def publicfilter(gallery, isAuthenticated=False):
    #return gallery.samplegallery(public=not isAuthenticated)



