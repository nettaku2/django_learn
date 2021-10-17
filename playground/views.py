from django.db.models.fields import DecimalField
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.models import Collection
from store.models import Order
from store.models import OrderItem
from store.models import Customer
from django.db.models import F, Q, Value, Func
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
import json
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def say_hello(request):
    # query_set = Product.objects.all()
    # for query in query_set:
    #     print(query)

    return HttpResponse('hello world')


def orm(request):
    collection = Product.objects.filter(description__isnull=True)
    # print(collection[0].orderitem)
    return render(request, 'orm.html',
                  {
                      'result': list(collection),
                  })


def say_hello2(request):
    query_set = Order.objects.select_related(
        'customer').values('id', 'customer__first_name').order_by('id').reverse()[:5]
    return render(request, 'hello.html', {'orders': list(query_set)})


def love_sabrina(request):
    return HttpResponse('I Love You, Sabrina')
