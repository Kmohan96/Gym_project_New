from django.db import models
from django.contrib.auth.models import User
class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainer_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.trainer_id
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField(null=True, blank=True)

    GOAL_CHOICES = [
        ("weight_loss", "Weight Loss"),
        ("muscle_gain", "Muscle Gain"),
        ("fitness", "General Fitness"),
    ]
    goal = models.CharField(
        max_length=20,
        choices=GOAL_CHOICES
    )

    gym_type = models.CharField(max_length=50)

    approved = models.BooleanField(default=False)

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
   

from django.db import models
from django.contrib.auth.models import User

class DailyUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    date = models.DateField()
    diet = models.CharField(max_length=200)
    attendance = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
