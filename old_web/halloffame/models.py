from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from datetime import datetime, date

# Game model which contains all games that are added to service


class Chat():
    id = models.CharField(max_length = 255)
    title = models.CharField(max_length=255)
    latestLeet = models.DateTimeField()


class TelegramUser():
    id = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)


class ChatMember():
    chat = models.ForeignKey(Chat, related_name="wat dis?", null=True)
    tg_user = models.ForeignKey(TelegramUser, related_name="dis wat?", null=True)
    prestige = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

