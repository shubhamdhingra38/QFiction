from django.shortcuts import render
from django.http import HttpResponse


def foo(request):
    # return HttpResponse("<h1>Hello there!</h1>")
    return render(request, 'main/index.html', context=None)
