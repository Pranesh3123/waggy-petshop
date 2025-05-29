from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product, ProductWeight, ProductSize
from .models import CartItem

@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'weight', 'size')
    total_price = sum(item.total_price for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart/cart.html', context)

@login_required(login_url='login')
def addproduct(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    weight_id = request.GET.get('weight_id')
    size_id = request.GET.get('size_id')
   
    weight = ProductWeight.objects.filter(id=weight_id, product=product).first() if weight_id else None
    size = ProductSize.objects.filter(id=size_id, product=product).first() if size_id else None
  
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        weight=weight,
        size=size,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def removeaddproduct(request,product_id ):
    cart_item =get_object_or_404(CartItem, id=product_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')  