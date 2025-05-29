from django.db import models
from django.contrib.auth.models import User
from products.models import Product,ProductWeight,ProductSize

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE)
    weight = models.ForeignKey(ProductWeight, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.name} in wishlist of {self.user.username}"
