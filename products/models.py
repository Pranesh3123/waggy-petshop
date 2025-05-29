from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    TAG_CHOICES = [
        ('Foods & Treats', 'Foods & Treats'),
        ('Toys', 'Toys'),
        ('Grooming', 'Grooming'),
        ('Beds & Furniture', 'Beds & Furniture'),
        ('Bowls & Feeders', 'Bowls & Feeders'),
        ('Health & Care', 'Health & Care'),
        ('Travel & Outdoor', 'Travel & Outdoor'),
        ('Clothing & Accessories', 'Clothing & Accessories'),
    ]
    ANIMAL_TYPE_CHOICES = [
        ('All', 'All'),
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Rabbit', 'Rabbit'),
        ('Bird', 'Bird'),
        ('Fish', 'Fish'),
        ('Turtle', 'Turtle'),
        ('Horse', 'Horse'),
        ('Reptile', 'Reptile'),
    ]

    tag = models.CharField(max_length=50, choices=TAG_CHOICES, default='Foods & Treats')
    type = models.CharField(max_length=50, choices=ANIMAL_TYPE_CHOICES, default='All')

    def __str__(self):
        return f"{self.tag} - {self.type}"

class Product(models.Model):
    product_id = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    brand = models.CharField(max_length=100,default='none')
    rating = models.PositiveSmallIntegerField(default=0, help_text="Rating from 1 to 5")
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_id} - {self.name}"
    
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg or 0, 1)

    def review_count(self):
        return self.reviews.count()

class ProductWeight(models.Model):
    product = models.ForeignKey(Product, related_name='weights', on_delete=models.CASCADE)
    weight_label = models.CharField(max_length=20, help_text="E.g., 250g, 500g, 1kg")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return f"{self.product.product_id} - {self.weight_label}"
        


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE,default='S')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.get_size_display()}"


class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE,default='None')
    color_name = models.CharField(max_length=30, help_text="E.g., Red, Blue, Green")
    hex_code = models.CharField(max_length=7, blank=True, null=True, help_text="Optional HEX code for display")

    def __str__(self):
        return f"{self.product.name} - {self.color_name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image of {self.product.product_id}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.product.name}"
