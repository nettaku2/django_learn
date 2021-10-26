from django.db.models import fields
from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    collection_id = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )
    # collection_title = serializers.StringRelatedField()

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField()

    # def count_products(self, collection):
    #     return collection.product_set.count()
    # fields = '__all__'
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(
#         max_digits=6, decimal_places=2, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax')
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail'
#     )

#     def calculate_tax(self, product: Product):
#         return round(product.unit_price * Decimal(1.1), 2)

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'title', 'description',
#                   'slug', 'inventory', 'price', 'price_with_tax', 'collection']

#     price = serializers.DecimalField(
#         max_digits=6, decimal_places=2, source='unit_price')

#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax')

#     # collection = serializers.HyperlinkedRelatedField(
#     #     queryset=Collection.objects.all(),
#     #     view_name='collection-detail'
#     # )

#     def calculate_tax(self, product: Product):
#         return round(product.unit_price * Decimal(1.1), 2)

    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
