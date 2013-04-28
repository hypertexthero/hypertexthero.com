"""
WSGI config for hth project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
# import os
# 
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hth.settings")
# 
# # This application object is used by any WSGI server configured to use this
# # file. This includes Django's development server, if the WSGI_APPLICATION
# # setting points here.
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
# 
# # Apply WSGI middleware here.
# # from helloworld.wsgi import HelloWorldApplication
# # application = HelloWorldApplication(application)
# 
# # http://andrew.io/weblog/2010/02/installing-django-with-virtualenv-on-dreamhost/
# # pkill python
# # touch ~/path/to/thisfile.py
# INTERP = os.path.join(os.environ['HOME'], 'Projects', 'hth-env', 'bin', 'python')
#     if sys.executable != INTERP:
#         os.execl(INTERP, INTERP, *sys.argv)

# https://my.a2hosting.com/knowledgebase.php?_m=knowledgebase&_a=viewarticle&kbarticleid=902
#Import sys and os modules
import sys, os
#We want virt_binary to point to our virtualenv binary
virt_binary = "/users/home/username/projects/virtualenvname/bin/python"
#The system python binary is not our virtualenv binary so we are going to execute our virtualenv python instead
if sys.executable != virt_binary: os.execl(virt_binary, virt_binary, *sys.argv)
sys.path.append(os.getcwd())
#This points the environment to our settings file as a relative path to the passenger_wsgi.py file
os.environ['DJANGO_SETTINGS_MODULE'] = "hth.settings"
#import our django stuff
import django.core.handlers.wsgi
#Tell passenger where the application is:
application = django.core.handlers.wsgi.WSGIHandler()