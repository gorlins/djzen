#!/usr/bin/python
# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from djzen.models import *
import os
from datetime import datetime
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.core.files import File
from django.db import settings

class Command(BaseCommand):
    help = ('Updates exif information for all photos.')

    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        return syncusers()#(args, options)

def syncusers():
    
