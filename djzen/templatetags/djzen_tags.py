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



