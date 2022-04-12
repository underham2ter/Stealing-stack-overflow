from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import AskForm, AnswerForm
from .models import Answer, Question


def question_list(response):
    user = response.user
    # if tab == 'new':
    #     questions = Question.objects.new()
    # elif tab == 'popular':
    #     questions = Question.objects.popular()
    questions = Question.objects.new()
    return render(response, 'questions/show_questions.html', {'questions': questions})


def question_page(response, q_id):
    params = {
        'title': Question.objects.get(id=q_id).title,
        'text': Question.objects.get(id=q_id).text,
        'author': Question.objects.get(id=q_id).author,
        'date': Question.objects.get(id=q_id).added_at,
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
