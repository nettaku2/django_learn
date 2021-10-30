from typing import Counter
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10

    list_filter = ['collection', 'last_update', InventoryFilter]
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} product were updated.',
            messages.INFO
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # url = (reverse('admin:store_product_changelist')
        #   + '?collection__id='
        #   + str(collection.id))
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

    # @admin.display(ordering='products_count')
    # def products_count(self, collection):
    #     url = (
    #         reverse('admin:store_product_changelist')
    #         + '?'
    #         + urlencode({
    #             'collection__id': str(collection.id)
    #         }))
    #     return format_html('<a href="{}">{}</a>', url, collection.products_count)

    # def get_queryset(self, request: HttpRequest) -> QuerySet:
    #     return super().get_queryset(request).annotate(
    #         products_count=Count('product'))

# Register your models here.


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name',
                    'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 10
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               })
               )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            orders_count=Count('order'))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 1
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = ['id', 'customer_first_name', 'customer_last_name']
    # list_select_related = ['customer']
    # ordering = ['id']

    # def customer_first_name(self, order):
    #     return order.customer.first_name

    # def customer_last_name(self, order):
    #     return order.customer.last_name

    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    ordering = ['id']
    inlines = [OrderItemInline]
