import django
from channels.routing import get_default_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dropdjango.settings")
django.setup()
application = get_default_application()