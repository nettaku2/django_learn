from django.db.models import fields
from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'price_with_tax', 'collection_number',
                  'collection_title', 'collection_object', 'collection_link']
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    collection_number = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(), source='collection'
    )
    collection_title = serializers.StringRelatedField(source='collection')
    collection_object = CollectionSerializer(source='collection')
    collection_link = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail',
        source='collection'
    )

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(
#         max_digits=6, decimal_places=2, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax')
#     collection_number = serializers.PrimaryKeyRelatedField(
#         queryset=Collection.objects.all(), source='collection'
#     )
#     collection_title = serializers.StringRelatedField(source='collection')
#     collection_object = CollectionSerializer(source='collection')
#     collection_link = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail',
#         source='collection'
#     )

#     def calculate_tax(self, product):
#         return product.unit_price * Decimal(1.1)
