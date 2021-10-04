from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.models import Collection
from store.models import OrderItem
from django.db.models import F
import json

# Create your views here.


def say_hello(request):
    # query_set = Product.objects.all()
    # for query in query_set:
    #     print(query)

    return HttpResponse('hello world')


def say_hello2(request):
    query_set = Product.objects.select_related('collection').all()
    return render(request, 'hello.html', {'products': list(query_set)})


def love_sabrina(request):
    return HttpResponse('I Love You, Sabrina')
