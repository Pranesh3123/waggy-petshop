from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from orders.models import Order,OrderItem
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserShippingAddress
from accounts.forms import UserProfileForm, ShippingAddressForm

def home(request):
    return render(request,'home.html')

def aboutus(request):
    return render(request,'aboutus.html')

def loginuser(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)

            if not UserShippingAddress.objects.filter(user=user).exists():
                return redirect('addshippingaddress')
            return redirect('userprofile')  # or 'home'
        else:
            messages.error(request, 'Invalid email or password.')
    context = {'page':page, 'hide_footer': True}
    return render(request, 'loginandregister.html',context)

def registeruser(request):
    page = 'register'
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'loginandregister.html', {'page': 'register'})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'loginandregister.html', {'page': 'register'})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'loginandregister.html', {'page': 'register'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = name
        user.save()
        login(request, user)

        return redirect('addshippingaddress')
    else:
        context = {'page':page}
        return render(request, 'loginandregister.html',context)

def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def userprofile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('userprofile')
    else:
        form = UserProfileForm(instance=user_profile)

    user_addresses = UserShippingAddress.objects.filter(user=user)
    user_orders = Order.objects.filter(user=user).order_by('-created_at')

    context = {
        'form': form,
        'user': user,
        'user_profile': user_profile,
        'user_addresses': user_addresses,
        'user_orders': user_orders,
    }
    return render(request, 'userprofile.html', context)

@login_required(login_url='login')
def addshippingaddress(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('userprofile')
    else:
        form = ShippingAddressForm()
    return render(request, 'addaddress.html', {'form': form})

@login_required(login_url='login')
def setdefaultshippingaddress(request, address_id):
    address = get_object_or_404(UserShippingAddress, id=address_id, user=request.user)

    # Unset previous defaults
    UserShippingAddress.objects.filter(user=request.user, default=True).update(default=False)

    # Set new default
    address.default = True
    address.save()
    return redirect('userprofile')

@login_required(login_url='login')
def edituserprofile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Update User model fields
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            # Update UserProfile model fields
            for field in ['phone', 'gender', 'date_of_birth', 'address', 'city', 'state', 'pincode', 'country']:
                setattr(profile, field, form.cleaned_data.get(field))

            # Handle new image upload
            new_image = form.cleaned_data.get('new_profile_picture')
            if new_image:
                profile.profile_picture = new_image

            profile.save()
            return redirect('userprofile')
    else:
        form = UserProfileForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': profile.phone,
            'gender': profile.gender,
            'date_of_birth': profile.date_of_birth,
            'address': profile.address,
            'city': profile.city,
            'state': profile.state,
            'pincode': profile.pincode,
            'country': profile.country,
        })

    return render(request, 'editform.html', {'form': form, 'user_profile': profile})

@login_required(login_url='login')
def editshippingaddress(request, address_id):
    address = get_object_or_404(UserShippingAddress, id=address_id, user=request.user)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('userprofile')
    else:
        form = ShippingAddressForm(instance=address)

    return render(request, 'editform.html', {'form': form, 'address_type': 'shipping'})

@login_required(login_url='login')
def deleteshippingaddress(request, address_id):
    address = get_object_or_404(UserShippingAddress, id=address_id, user=request.user)
    address.delete()
    return redirect('userprofile')