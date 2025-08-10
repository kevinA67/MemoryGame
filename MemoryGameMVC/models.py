from django.db import models
from django.contrib.auth.models import User

class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField()
    won = models.BooleanField()
    # NUEVO: nivel jugado (1=Fácil, 2=Medio, 3=Difícil)
    level = models.PositiveSmallIntegerField(default=1)
    # NUEVO: duración de la partida en segundos (tiempo utilizado)
    duration_seconds = models.PositiveIntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usuario = self.user.username if self.user else "Anónimo"
        estado = "Ganó" if self.won else "Perdió"
        return f"{usuario} - {estado} - {self.score} pts - L{self.level} - {self.duration_seconds}s"
