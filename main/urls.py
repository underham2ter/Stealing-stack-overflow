from django. urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.question_list, name='question_list'),
    path('question/', views.question_page, name='question_page'),
    path('signup/', views.sign_up, name='sign_up'),
    # path('auth/', views.auth, name='auth'),
    path('ask/', views.question_create, name='question_create')
]
