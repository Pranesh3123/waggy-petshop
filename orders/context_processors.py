from .models import Order

def order_count(request):
    if request.user.is_authenticated:
        count = Order.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'order_count': count}
