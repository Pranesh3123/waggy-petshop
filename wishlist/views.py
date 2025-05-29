from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product, ProductWeight, ProductSize
from .models import WishlistItem

@login_required(login_url='login')
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product', 'weight', 'size')
    context = {'wishlist_items': wishlist_items}
    return render(request, 'wishlist/wishlist.html', context)

@login_required(login_url='login')
def addwishproduct(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    weight_id = request.GET.get('weight_id')
    size_id = request.GET.get('size_id')
    print(weight_id)
    weight = ProductWeight.objects.filter(id=weight_id, product=product).first() if weight_id else None
    size = ProductSize.objects.filter(id=size_id, product=product).first() if size_id else None
    print(weight)
    wishlist_item, created = WishlistItem.objects.get_or_create(
        user=request.user,
        product=product,
        weight=weight,
        size=size,
    )

    if not created:
        wishlist_item.save()

    return redirect('wishlist')

@login_required(login_url='login')
def removewishproduct(request,item_id ):
    wishlist_item =get_object_or_404(WishlistItem, id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist') 

@login_required(login_url='login')
def wishlistcount(request):
    if request.user.is_authenticated:
        count = WishlistItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return JsonResponse({'count': count})
