from .models import Product
def products_details(request):
    products = Product.objects.all() 
    return {'products': products}
