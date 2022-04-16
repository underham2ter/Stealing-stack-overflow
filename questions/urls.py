from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('ask/', views.question_create, name='question_create'),
    path('<int:q_id>/', views.question_page, name='question_page'),
]


