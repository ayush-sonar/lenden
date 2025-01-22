from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class Game(models.Model):
    STATUS_ENUM = [
        ('P', 'Pending'),
        ('A', 'Active'),
        ('F', 'Finished'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    p1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='p1')
    p2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='p2')
    status = models.CharField(max_length=1, choices=STATUS_ENUM, default='P')
    canvas = models.JSONField(default=dict)
    currentTurn = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='currentTurn')
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='winner', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.p1} vs {self.p2}'
    
class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    move_number = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['move_number']
    

