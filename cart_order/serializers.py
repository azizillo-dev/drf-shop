from rest_framework import serializers
from .models import Cart, Order, OrderItem


class CartSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_title', 'price', 'quantity', 'total_price']
        read_only_fields = ['id']



class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'price']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'address', 'total_price', 'status', 'created_at', 'items']
        read_only_fields = ['id', 'total_price', 'status', 'created_at']
