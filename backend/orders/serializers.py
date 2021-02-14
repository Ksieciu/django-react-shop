from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Order, OrderItem, ShippingAddress
from accounts.serializers import UserSerializer

ORDER_PLACED = 'PLACED'
IN_REALIZATION = 'REALIZATION'
SENT = 'SENT'
CANCELLED = 'CANCELLED'
COMPLETED = 'COMPLETED'
ORDER_STATUS = [
    (ORDER_PLACED, 'Order placed'),
    (IN_REALIZATION, 'In realization'),
    (SENT, 'Order sent'),
    (CANCELLED, 'Cancelled'),
    (COMPLETED, 'Completed'),
]


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shipping_address = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shipping_address(self, obj):
        try:
            address = ShippingAddressSerializer(
                    obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        print(user)
        serializer = UserSerializer(user, many=False)
        return serializer.data