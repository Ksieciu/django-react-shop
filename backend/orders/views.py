from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderItem, ShippingAddress
from .serializers import OrderSerializer
from core.models import Product
from core.serializers import ProductSerializer
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    order_items = data['orderItems']

    if order_items and len(order_items) == 0:
        return Response({'detail': 'No Order Items'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            payment_method=data['paymentMethod'],
            tax_amount=data['taxPrice'],
            shipping_price=data['shippingPrice'],
            total_price=data['totalPrice']
        )

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postcode=data['shippingAddress']['postcode'],
            country=data['shippingAddress']['country']
        )

        for i in order_items:
            product = Product.objects.get(id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i['quantity'],
                price=i['price'],
                image=product.image.url
            )

            product.count_in_stock -= item.quantity
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user
    try:
        order = Order.objects.get(id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not authorized to view this order'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, 
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_payment_status(request, pk):
    order = Order.objects.get(id=pk)

    order.payment_done = True
    order.payment_date = datetime.now()
    order.save()
    return Response('Payment done')