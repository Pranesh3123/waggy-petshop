from .models import CartItem

def cart_data(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'weight', 'size')
        total_price = sum(item.total_price for item in cart_items)
    else:
        cart_items = []
        total_price = 0  # ✅ set 0 instead of 1
    
    return {
        'cart_items': cart_items,
        'total_price': total_price,
    }
