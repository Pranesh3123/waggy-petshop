from django.db import models
from django.contrib.auth.models import User
from products.models import Product, ProductSize, ProductWeight

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE)
    weight = models.ForeignKey(ProductWeight, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.user.username}'s cart"
    
    @property
    def total_price(self):
        price = 0
        if self.weight and self.weight.discount_price:
            price = self.weight.discount_price
        elif self.size and self.size.discount_price:
            price = self.size.discount_price
        else:
            if self.weight:
                price = self.weight.price
            elif self.size:
                price = self.size.price
        return price * self.quantity
    
    @property
    def subtotal(self):
        if self.weight and self.weight.discount_price:
            return self.quantity * self.weight.discount_price
        elif self.size and self.size.discount_price:
            return self.quantity * self.size.discount_price
        elif self.weight:
            return self.quantity * self.weight.price
        elif self.size:
            return self.quantity * self.size.price
        return 0 
