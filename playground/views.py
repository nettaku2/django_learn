from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.models import Collection
from store.models import Order
from store.models import OrderItem
from django.db.models import F, Q
import json
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def say_hello(request):
    # query_set = Product.objects.all()
    # for query in query_set:
    #     print(query)

    return HttpResponse('hello world')

def orm(request):
    collections = Collection.objects.all().order_by('id')
    for collection in list(collections):
        print(collection.title)

    print('==========================')
    collection = Collection.objects.get(pk=2)
    print(f'id: {collection.id}, title: {collection.title}')

    products = Product.objects.filter(last_update__year=2020)

    try:
        product = Product.objects.get(id=0)
    except ObjectDoesNotExist:
        product = { 'title': 'sabrina' }
    # product = Product.objects.filter(id=0).exists()
    # print(product)

    # products = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # products = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # products = Product.objects.filter(~Q(inventory__lt=10) & Q(unit_price__lt=20))
    # products = Product.objects.filter(inventory=F('collection__title'))
    products = Product.objects.all().order_by('id')

    return render(request, 'orm.html',
    {
        'name': 'harry',
        'age': 48,
        'collections': list(collections),
        'collection': collection,
        'products': products,
        'product': product
    })


def say_hello2(request):
    query_set = Order.objects.select_related(
        'customer').values('id', 'customer__first_name').order_by('id').reverse()[:5]
    return render(request, 'hello.html', {'orders': list(query_set)})


def love_sabrina(request):
    return HttpResponse('I Love You, Sabrina')
