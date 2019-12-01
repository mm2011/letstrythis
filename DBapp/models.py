from django.db import models


# Create your models here.
class Question(models.Model):
    questionID = models.PositiveIntegerField(default=0)
    questionText = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.questionID} {self.questionText}"


class Answer(models.Model):
    questionID = models.IntegerField(default=0)
    answerText = models.CharField(max_length=200)
    isRight = models.BooleanField()

    def __str__(self):
        return f"{self.questionID} {self.answerText} {self.isRight}"









