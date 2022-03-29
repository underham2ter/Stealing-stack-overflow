from django.db import models, connection
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    added_at = models.DateField()
    rating = models.IntegerField()
    author = models.CharField(max_length=20)
    likes = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question', null=True)


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField()
    question = models.TextField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer', null=True)

