from django.contrib import admin
from .models import Category, Product, ProductImage, ProductWeight,ProductSize,ProductColor,Review

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductWeight)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(ProductImage)
admin.site.register(Review)

