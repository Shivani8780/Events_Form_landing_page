import os
import sys

# Add your project directory to the sys.path
project_home = '/home/Shivani19/my_event_form_project/Events_Form_landing_page/Events_Form_landing_page'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'biodata_project.settings'

# Import Django's WSGI application handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
