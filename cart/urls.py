from django.urls import path
from . import views

urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('addproduct/<str:product_id>/', views.addproduct, name='addproduct'),
    path('removeaddproduct/<str:product_id>/',views.removeaddproduct,name='removeaddproduct'),
]
