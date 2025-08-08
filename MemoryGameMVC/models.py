from django.db import models

class GameResult(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Fácil'),
        ('medium', 'Media'),
        ('hard', 'Difícil'),
    ]

    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    won = models.BooleanField()  # True si ganó, False si perdió
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Ganó" if self.won else "Perdió"
        return f"{estado} en {self.get_difficulty_display()} - {self.played_at.strftime('%Y-%m-%d %H:%M')}"
