#!/usr/bin/python
# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
from djzen.models import *
from time import time
from django.db import settings
import zenapi

class Command(BaseCommand):
    help = ('Updates exif information for all photos.')

    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        return addusers(*args)#(args, options)

def addusers(*users):
    for u in users:
        try:
            user = User.objects.get(LoginName=u)
            print 'Updating', user.LoginName
        except User.DoesNotExist:
            user = User(LoginName=u)
            print 'Adding', user.LoginName
        t0 = time()
        user.update(updateChildren=True)
        user.save()
        print 'Success!!!'
        print 'Time elapsed: %s seconds'%(time()-t0)
        
