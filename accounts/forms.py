from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile,UserShippingAddress
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    new_profile_picture = forms.ImageField(required=False, label='Upload New Profile Picture')

    class Meta:
        model = UserProfile
        fields = ['phone', 'gender', 'date_of_birth', 'address', 'city', 'state', 'pincode', 'country', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Format: yyyy-mm-dd',
                    'type': 'date'  # 
                }
            ),
        }
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = UserShippingAddress
        fields = ['address_type', 'phone', 'address', 'city', 'state', 'pincode', 'country']

