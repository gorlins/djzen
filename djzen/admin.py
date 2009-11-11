""" Newforms Admin configuration for djzen

"""
from django.contrib import admin
from models import *

class UserAdmin(admin.ModelAdmin):
    list_display=('LoginName', 'DisplayName', 'DomainName')
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ('Title', 'zenlink', 'Owner')
    list_filter=['Owner', 'CreatedOn']
    #list_filter = ['date_added', 'is_public']
    #search_fields = ['title', 'description']
    #date_hierarchy = 'date_added'
    #prepopulated_fields = {'title_slug': ('title',)}
    ##filter_horizontal = ('photos',)
    
class PhotoSetAdmin(admin.ModelAdmin):
    list_display = ('Title', 'adminthumb', 'Type', 'zenlink', 'Owner')
    list_filter=['Type', 'Owner', 'CreatedOn']
    
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('Title', 'adminthumb', 'FileName', 'Gallery', 'TakenOn',
                    'zenlink', 'Owner')
    list_filter = ['TakenOn', 'Owner', 'Gallery']
    #search_fields = ['title', 'description', 'foldername']
    #date_hierarchy = 'date_added'
    #prepopulated_fields = {'slug': ('foldername',)}
    #actions = [publishFolderContents, unpublishFolderContents]

#class AutoCollectionAdmin(admin.ModelAdmin):
    #list_display = ('title', 'admin_thumb', 'date_added', 'is_public')
    #list_filter = ['date_added', 'is_public']
    #search_fields = ['title', 'description', 'queryfield']
    #date_hierarchy = 'date_added'
    #prepopulated_fields = {'slug': ('title',)}


#class PhotoAdmin(admin.ModelAdmin):
    ##list_display = ('title', 'date_taken', 'date_added', 'is_public', 'tags', 'view_count', 'admin_thumbnail')
    #list_display = ('admin_thumb', 'title', 'image', 'is_public', 'num_views', 'parent')
    #list_filter = ['date_added', 'date_taken', 'is_public', 'parent']
    #search_fields = ['title', 'caption']
    #list_per_page = 10
    #prepopulated_fields = {'slug': ('title',)}
    ##prepopulated_fields = {'title_slug': ('title',)}
    ##filter_horizontal = ('public_galleries',)

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(PhotoSet, PhotoSetAdmin)
admin.site.register(Photo, PhotoAdmin)