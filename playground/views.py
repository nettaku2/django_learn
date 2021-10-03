from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def say_hello(request):
    return HttpResponse('Hello World')


def say_hello2(request):
    return render(request, 'hello.html')


def love_sabrina(request):
    return HttpResponse('I Love You, Sabrina')
