# models.py
from django.db import models
from django.contrib.auth.models import User

class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    won = models.BooleanField()
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Ganó' if self.won else 'Perdió'} - {self.score}"
