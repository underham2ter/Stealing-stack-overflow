
from django.db import models, connection
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name="question_author", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_by')
    dislikes = models.ManyToManyField(User, related_name='disliked_by')
    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question, related_name="q_to_ans", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="answer_author", on_delete=models.CASCADE)

