from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserShippingAddress
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(UserShippingAddress, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=100, default='Dummy Pay')
    status = models.CharField(
        max_length=50,
        choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')],
        default='processing'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, to_field='product_id', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
