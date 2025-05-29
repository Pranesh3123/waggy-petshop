from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from cart.models import CartItem
from orders.models import Order, OrderItem
from accounts.models import UserShippingAddress

@login_required(login_url='login')
def orders(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            quantity_key = f'quantity_{item.id}'
            if quantity_key in request.POST:
                try:
                    new_quantity = int(request.POST[quantity_key])
                    if new_quantity > 0:
                        item.quantity = new_quantity
                        item.save()
                except ValueError:
                    continue
        return redirect('orders') 

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal for item in cart_items)

    # get the default shipping address or first address
    user = request.user
    default_address = UserShippingAddress.objects.filter(user=user, default=True).first()

    if not default_address:
        default_address = UserShippingAddress.objects.filter(user=user).first()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'default_address': default_address
    }
    return render(request, 'orders/orders.html', context)
@login_required(login_url='login')
def orderdetails(request):
    if request.method == "POST":
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            return redirect('cart')
    
        total_price = 0

        for item in cart_items:
            price = 0
            if hasattr(item, 'weight') and item.weight:
                price = item.weight.discount_price if item.weight.discount_price else item.weight.price
            elif hasattr(item, 'size') and item.size:
                price = item.size.discount_price if item.size.discount_price else item.size.price

            total_price += price * item.quantity
        total_price += 250  # Shipping or additional charge

        payment_method = request.POST.get("payment_method", "Not Specified")

        shipping_address = UserShippingAddress.objects.filter(user=request.user, default=True).first()
        if not shipping_address:
            shipping_address = UserShippingAddress.objects.filter(user=request.user).first()


        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            total_price=total_price,
            payment_method=payment_method
        )
        for item in cart_items:
            if item.weight:
                price = item.weight.discount_price if item.weight.discount_price is not None else item.weight.price
            elif item.size:
                price = item.size.discount_price if item.size.discount_price is not None else item.size.price
            else:
                price = 0  

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=price
            )
            item.delete()
                
        messages.success(request, "🎉 Your order has been placed successfully!")

    return redirect('userorders')
@login_required(login_url='login')
def useroders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    for order in orders:
        time_diff = timezone.now() - order.created_at

        if order.status == 'processing' and time_diff > timedelta(days=1):
            order.status = 'shipped'
            order.save()
        elif order.status == 'shipped' and time_diff > timedelta(days=3):
            order.status = 'delivered'
            order.save()
    context ={'userorders':orders}
    return render(request,'orders/userorders.html',context)
@login_required(login_url='login')
def vieworderproduct(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/vieworderproduct.html', {'order': order})
@login_required(login_url='login')
def cancelorder(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Check if status allows cancellation
    if order.status.lower() in ['processing', 'shipped']:
        order.delete()
        messages.success(request, "Order has been cancelled successfully.")
    else:
        messages.error(request, "Order cannot be cancelled at this stage.")

    return redirect('userorders')

