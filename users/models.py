import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username or f"Telegram user {self.telegram_id}"


class TelegramToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    session_key = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Token: {self.token}'
