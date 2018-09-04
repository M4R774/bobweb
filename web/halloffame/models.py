from django.db import models


class Chat():
    id = models.CharField(max_length = 255)
    title = models.CharField(max_length=255)
    latestLeet = models.DateTimeField()
    botUpTimeStart = models.DateTimeField()  # date since last reboot, used for up time calculations
    messageCount = models.PositiveIntegerField(default=0)


class TelegramUser():
    id = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)


# Chat members tie the users and chats. TelegramUser can be in many different chats with different ranks.
class ChatMember():
    chat = models.ForeignKey(Chat, related_name="wat dis?", null=True)
    tg_user = models.ForeignKey(TelegramUser, related_name="dis wat?", null=True)  # is there a way to restrict that only one instanse of a user/chat?
    prestige = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

