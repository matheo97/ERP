#coding=utf-8
import os
import sys

path = '/home/matt9742/trabajogrado'  # aquí utiliza tu propio usuario, sin los simbolos < y >
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'solteca.settings'

# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
#import os
#import sys
#
## assuming your django settings file is at '/home/matt9742/mysite/mysite/settings.py'
## and your manage.py is is at '/home/matt9742/mysite/manage.py'
#path = '/home/matt9742/mysite'
#if path not in sys.path:
#    sys.path.append(path)
#
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
#
## then, for django >=1.5:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
## or, for older django <=1.4
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()