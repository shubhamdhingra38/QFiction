from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', foo),
    path('ask-question/<str:book_name>/<int:book_num>/', ask_ques),
    path('books/<str:book_name>/', bar),
    # path('books/<str:book_name>/<int:id>/', foobar),
]
