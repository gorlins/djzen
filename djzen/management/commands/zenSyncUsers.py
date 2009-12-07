#!/usr/bin/python
# coding: utf-8
"""Adds or syncs a Zenfolio user with the database

Note that this may take awhile the first time it's called, but will be faster
on subsequent calls (as select_related comes in useful), but it will load
practically the entire database into memory..."""
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
        return syncusers(*args)#(args, options)

def syncusers(*users):
    for u in users:
        try:
            # Can't call get cause need QuerySet for select_related???
            user = User.objects.filter(LoginName=u).select_related()[0]
            print 'Updating', user.LoginName
        except IndexError:
            user = User(LoginName=u)
            print 'Adding', user.LoginName
        t0 = time()
        user.update(updateChildren=True)
        user.save()
        print 'Success!!!'
        print 'Time elapsed: %s seconds'%(time()-t0)
        
