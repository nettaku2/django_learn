from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline

class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 1

class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedItemInline]
# Register your models here.

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)