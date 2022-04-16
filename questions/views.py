from django.contrib.auth.decorators import login_required
from django.core.mail.backends import console
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import AskForm, AnswerForm
from .models import Answer, Question
import json
import pdb
import logging

logger = logging.getLogger(__name__)


def question_list(response):
    tab = response.GET.get('tab')
    if tab == 'new':
        questions = Question.objects.new()
    else:
        questions = Question.objects.popular()
    return render(response, 'questions/show_questions.html', {'questions': questions})


def question_page(response, q_id):
    question = Question.objects.get(id=q_id)
    user = response.user
    al = user in question.likes.all()
    adl = user in question.dislikes.all()
    answers = question.q_to_ans.all()

    if response.method == "POST":
        liked = question.likes.filter(id=user.id)
        disliked = question.dislikes.filter(id=user.id)
        if 'answer_submit' in response.POST:
            form = AnswerForm(response.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.author = user
                answer.question = question
                answer.save()
            return HttpResponseRedirect('/questions/{id}'.format(id=question.id))
        elif response.POST.get("operation") == "upvote" and response.accepts('ajax'):
            if liked:
                question.likes.remove(user)
                question.rating -= 1
                liked = False
                disliked = False
                question.save()
            else:
                if not disliked:
                    question.rating += 1
                else:
                    question.rating += 2
                question.likes.add(user)
                question.dislikes.remove(user)
                liked = True
                disliked = False
                question.save()
            ctx = {"rating": question.rating, "liked": liked, 'disliked': disliked}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        elif response.POST.get("operation") == "downvote" and response.accepts('ajax'):
            if disliked:
                question.dislikes.remove(user)
                question.rating += 1
                disliked = False
                liked = False
                question.save()
            else:
                if not liked:
                    question.rating -= 1
                else:
                    question.rating -= 2

                question.dislikes.add(user)
                question.likes.remove(user)
                disliked = True
                liked = False
                question.save()
            ctx = {"rating": question.rating, "liked": liked, 'disliked': disliked}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        form = AnswerForm()
        params = {
            'form': form,
            'question': question,
            'already_liked': al,
            'already_disliked': adl,
        }
        return render(response, 'questions/question_page.html', params)


@login_required
def question_create(response):
    user = response.user

    if response.method == 'POST':
        form = AskForm(response.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = user
            question.save()
            return HttpResponseRedirect('/questions/{id}'.format(id=question.id))

    else:
        form = AskForm()
        return render(response, 'questions/question_create.html', {'form': form})
