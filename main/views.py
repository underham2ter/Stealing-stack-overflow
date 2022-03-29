from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(response):
    return render(response, 'main/index.html')


def question_list(response):
    return HttpResponse('<div>Hello!</div>')


def question_page(response):
    return HttpResponse('<div>Hello!</div>')


def sign_up(response):
    return HttpResponse('<div>sign_up</div>')


# def auth(response):
#     return render(response, 'main/auth.html', {'name': 'kek auth'})


def question_create(response):
    return HttpResponse('<div>question_create</div>')
