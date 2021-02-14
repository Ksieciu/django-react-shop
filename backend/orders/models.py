import datetime
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Product

User = settings.AUTH_USER_MODEL

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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    tax_amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    shipping_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=11, choices=ORDER_STATUS, default='PLACED')
    payment_done = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    sending_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    received_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.order_date}'

@receiver(pre_save, sender=Order)
def on_change(sender, instance: Order, **kwargs):
    '''
    Automatically changes send, cancelled 
    and completed dates when status changes
    (change for status change date if date
    was not specified in save())
    '''
    try:
        prev_order = Order.objects.get(id=instance.id)
        if prev_order.status != instance.status:
            if instance.status == 'SENT' and prev_order.send_date == instance.send_date:
                instance.send_date = datetime.datetime.now()
            elif instance.status == 'CANCELLED' and prev_order.cancellation_date == instance.cancellation_date:
                instance.cancellation_date = datetime.datetime.now()
            elif instance.status == 'COMPLETED' and prev_order.completed_date == instance.completed_date:
                instance.completed_date = datetime.datetime.now()
    except:
        pass

    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.address
    
