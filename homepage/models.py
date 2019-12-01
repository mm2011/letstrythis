from django.db import models
from django.contrib.auth.models import User, auth


class People(models.Model):
    username = models.CharField(max_length=30)
    firstName = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.username}, {self.firstName}"


class Score(models.Model):
    username = models.CharField(max_length=30)
    numQuestions = models.PositiveIntegerField(default=0)
    numCorrect = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.username}: {self.numCorrect}/{self.numQuestions}"