import sys
from django.utils import timezone
from django.db.models import Max
from django.db.models import Sum
sys.path.append('../web')  # needed for sibling import
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web.settings"
)
from django.conf import settings
django.setup()
from halloffame.models import *


# Checks the reminders
def check_reminders():
    pass