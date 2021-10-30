from django.db.models import fields
from rest_framework import serializers
from decimal import Decimal
from .models import Cart, CartItem, Product, Collection, Customer, Order, OrderItem, Review
from uuid import uuid4


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
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

    user_id = serializers.IntegerField(read_only=True)


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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']

    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cartitem):
        return Decimal(cartitem.quantity) * cartitem.product.unit_price

    product = SimpleProductSerializer()


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "No Product with the given id was found")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

        return super().save(**kwargs)

    product_id = serializers.IntegerField()


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'cartitem_set', 'total_price']

    id = serializers.UUIDField(read_only=True)
    cartitem_set = CartItemSerializer(many=True, read_only=True)
    # created_at = serializers.DateTimeField(read_only=True)

    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.cartitem_set.all()])
