import sys
import os
from datetime import datetime


# Checks the reminders
def check_reminders(bot):
    pass
    # reminders = Reminder.objects.filter(date__lte=datetime.now())
    # for reminder in reminders:
    #     reply = 'Muista: ' + str(reminder.remember_this)
    #     bot.sendMessage(reminder.chat.id, reply)
    # reminders.delete()
