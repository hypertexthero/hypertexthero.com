import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hth.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# alternate config for trying uWSGI at some point

# import os, sys
# 
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
# 
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hth.settings")
# 
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()