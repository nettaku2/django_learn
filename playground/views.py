from django.db.models.fields import DecimalField
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.models import Collection
from store.models import Order
from store.models import OrderItem
from store.models import Customer
from store.models import Address
from store.models import Cart, CartItem
from django.db.models import F, Q, Value, Func, ExpressionWrapper
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
import json
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
from tags.models import TaggedItem
from django.db import transaction
from django.db import connection

# Create your views here.


def say_hello(request):
    # query_set = Product.objects.all()
    # for query in query_set:
    #     print(query)

    return HttpResponse('hello world')


def orm(request):

    queryset = Product.objects.annotate(
        total_sales=Sum(F('orderitem__quantity') *
                        F('orderitem__unit_price'))
    ).order_by('-total_sales')[:5]

    return render(request, 'orm.html',
                  {
                      'result': list(queryset),
                  })


def product_list(request):
    queryset = Product.objects.all()
    return render(request, 'template.html', {'result': list(queryset)})


def say_hello2(request):
    query_set = Order.objects.select_related(
        'customer').values('id', 'customer__first_name').order_by('id').reverse()[:5]
    return render(request, 'hello.html', {'orders': list(query_set)})


def love_sabrina(request):
    return HttpResponse('I Love You, Sabrina')
