from django.db.models import fields
from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection, Customer, Order, OrderItem, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price', 'order', 'product']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone', 'birth_date', 'membership']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    # products_count = serializers.IntegerField()

    products_count = serializers.SerializerMethodField('count_products')

    def count_products(self, collection):
        return collection.product_set.count()

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField(required=False)
#     title = serializers.CharField(max_length=255)
#     products_count = serializers.SerializerMethodField('count_products')

#     def count_products(self, collection):
#         return collection.product_set.count()

#     def create(self, validated_data):
#         collection = Collection(**validated_data)
#         collection.save()
#         return collection

#     def update(self, instance, validated_data):
#         instance.title = validated_data["title"]
#         instance.save()
#         return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description',
                  'inventory', 'price', 'price_with_tax', 'last_update', 'collection']
        # fields = ['id', 'title', 'price', 'price_with_tax', 'collection_number',
        #           'collection_title', 'collection_object', 'collection_link']
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    # collection_number = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all(), source='collection'
    # )
    # collection_title = serializers.StringRelatedField(source='collection')
    # collection_object = CollectionSerializer(source='collection')
    # collection_link = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail',
    #     source='collection'
    # )

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)

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
    #     instance.other = 1
    #     instance.save()
    #     return instance

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
