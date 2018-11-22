from django.db import models

# TODO: Remember to change the secret key from settings.py
# TODO: lisää viisaus ominaisuus


class TelegramUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    nickname = models.CharField(max_length=255, null=True)
    firstName = models.CharField(max_length=255, null=True)
    lastName = models.CharField(max_length=255, null=True)

    def __str__(self):
        if self.nickname is not None:
            return str(self.nickname)
        elif self.lastName is not None:
            return str(self.lastName)
        elif self.firstName is not None:
            return str(self.firstName)
        else:
            return str(self.id)


class Chat(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, null=True)
    latestLeet = models.DateField(null=True)
    botUpTimeStart = models.DateTimeField(null=True)  # date since last reboot, used for up time calculations
    messageCount = models.PositiveIntegerField(default=0)
    members = models.ManyToManyField(
        TelegramUser,
        through='ChatMember',
        through_fields=('chat', 'tg_user'),
    )
    # TODO: Add fields "feature_x_enabled", for example leetEnable, for enabling
    # and disabling leet counting for each chat seperately.

    def __str__(self):
        return str(self.id)


# Chat members tie the users and chats. TelegramUser can be in many different chats with different ranks.
class ChatMember(models.Model):
    chat = models.ForeignKey('Chat', null=False, on_delete=models.CASCADE)
    tg_user = models.ForeignKey('TelegramUser', null=False, on_delete=models.CASCADE)
    prestige = models.PositiveIntegerField(default=0)
    _rank = models.PositiveIntegerField(default=0)

    @property
    def rank(self):
        return self._rank

    class Meta:
        unique_together = ("chat", "tg_user")
        ordering = ['-_rank', '-prestige']

    def __str__(self):
        return str(self.rank)

    # TODO: Return the rank as string
    def rank_str(self):
        f = open('ranks.txt')
        lines = f.readlines()
        return str(lines[self.rank])


# Viisaus
class Proverb(models.Model):
    proverb = models.TextField(unique=True)
    author = models.CharField(max_length=255, null=True)
    send_count = models.PositiveIntegerField(default=0) # How many times the proverb has been sent
    date = models.DateField(null=True)

    class Meta:
        ordering = ['send_count']

    def __str__(self):
        return str(self.proverb)

# Reminder objects here?