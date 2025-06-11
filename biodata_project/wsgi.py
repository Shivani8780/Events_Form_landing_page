import os
import sys

# add your project directory to the sys.path
project_home = '/home/BhudevNetwork/Events_Form_landing_page'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set environment variable to tell django where your settings.py is
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biodata_project.settings')

# serve django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
