from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User
from django.forms import ModelForm


class AskForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
