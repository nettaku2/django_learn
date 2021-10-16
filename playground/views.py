from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.models import Collection
from store.models import Order
from store.models import OrderItem
from store.models import Customer
from django.db.models import F, Q, Value
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
import json
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def say_hello(request):
    # query_set = Product.objects.all()
    # for query in query_set:
    #     print(query)

    return HttpResponse('hello world')


def orm(request):
    result = Customer.objects.annotate(
        full_name=F('first_name'))
    return render(request, 'orm.html',
                  {
                      'result': list(result),
                  })


def say_hello2(request):
    query_set = Order.objects.select_related(
        'customer').values('id', 'customer__first_name').order_by('id').reverse()[:5]
    return render(request, 'hello.html', {'orders': list(query_set)})


def love_sabrina(request):
    return HttpResponse('I Love You, Sabrina')
