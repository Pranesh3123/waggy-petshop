from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Category, Product, ProductImage, ProductWeight,ProductSize,ProductColor,Review
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Avg, Count
import  random
@login_required(login_url='login')
def recommended_and_bestselling_products(request):
    # for recommended products
    top_rated = Product.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=4).order_by('-avg_rating')[:8]

    if top_rated.count() < 8:
        needed = 8 - top_rated.count()
        fallback = Product.objects.filter(is_available=True).exclude(id__in=top_rated.values_list('id', flat=True)).order_by('-created_at')[:needed]
        recommendedproducts = list(top_rated) + list(fallback)
    else:
        recommendedproducts = list(top_rated)

    # for best selling products
    available_products = list(Product.objects.filter(is_available=True))
    random.shuffle(available_products)
    bestselling = available_products[:8]
    paginator = Paginator(bestselling, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'recommendedproducts': recommendedproducts,
        'bestsellingproducts': page_obj,
        'productImg': ProductImage.objects.all(),
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
def shop(request):
    tag_choices = Category.TAG_CHOICES
    animal_type_choices = Category.ANIMAL_TYPE_CHOICES

    category_filter = request.GET.getlist('category')   # Animal types
    tag_filter = request.GET.getlist('tag')             # Tags
    brand_filter = request.GET.getlist('brand')         # Brand names
    price_filter = request.GET.getlist('price')         # Price ranges

    accessory_filter = request.GET.getlist('accessories')
    products = Product.objects.filter(is_available=True)

    if accessory_filter:
        products = products.filter(category__tag__in=accessory_filter)


    # Apply filters
    if category_filter and 'All' not in category_filter:
        products = products.filter(category__type__in=category_filter)

    if tag_filter:
        products = products.filter(category__tag__in=tag_filter)

    if brand_filter:
        products = products.filter(brand__in=brand_filter)

    if price_filter:
        price_q = Q()
        for price_range in price_filter:
            if price_range == 'Under ₹500':
                price_q |= Q(weights__price__lt=500) | Q(sizes__price__lt=500)
            elif price_range == '₹500 – ₹1000':
                price_q |= (Q(weights__price__gte=500, weights__price__lte=1000) |
                            Q(sizes__price__gte=500, sizes__price__lte=1000))
            elif price_range == '₹1000 – ₹2000':
                price_q |= (Q(weights__price__gte=1000, weights__price__lte=2000) |
                            Q(sizes__price__gte=1000, sizes__price__lte=2000))
            elif price_range == '₹2000+':
                price_q |= Q(weights__price__gt=2000) | Q(sizes__price__gt=2000)
        products = products.filter(price_q).distinct()
        
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__tag__icontains=query) | 
            Q(category__type__icontains=query) | 
            Q(brand__icontains=query)
        )
    available_brands = Product.objects.filter(is_available=True).values_list('brand', flat=True).distinct()


    # Pagination
    paginator = Paginator(products.distinct(), 12)
    page_no = request.GET.get('page')
    product = paginator.get_page(page_no)

    context = {
        'product': product,
        'productImg': ProductImage.objects.all(),
        'tag_choices': tag_choices,
        'animal_type_choices': animal_type_choices,
        'available_brands': available_brands,
        'search_query': query or ''
    }
    return render(request, 'products/shop.html', context)

@login_required(login_url='login')
def viewproduct(request,product_id):
    product = get_object_or_404(Product,product_id=product_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('review_text')
        name = request.POST.get('review_name')

        if request.user.is_authenticated:
            Review.objects.create(
                user = request.user,
                product = product,
                rating = rating,
                comment =comment,
            )
            messages.success(request, "Your review has been submitted.")
            return redirect('viewproduct',product_id=product_id)
        else:
            messages.error(request, "Your review has been submitted.")
            return redirect('login')
        
    reviews = product.reviews.all()
    rating_stats = reviews.aggregate(avg_rating=Avg('rating'), total_reviews=Count('id'))
    avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = rating_stats['total_reviews']



    context = {
        'product': product,
        'avg_rating': round(avg_rating, 1),
        'total_reviews': total_reviews,
    }
    return render(request,'products/viewproduct.html',context)

