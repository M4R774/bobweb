import sys
import os
from datetime import datetime
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
def check_reminders(bot):
    reminders = Reminder.objects.filter(date__lte=datetime.now())
    for reminder in reminders:
        reply = 'Muista: ' + str(reminder.remember_this)
        bot.sendMessage(reminder.chat.id, reply)
    reminders.delete()
