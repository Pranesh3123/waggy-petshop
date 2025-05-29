from django.urls import path
from . import views

urlpatterns = [
    path('orders/',views.orders,name='orders'),
    path('orderdetails/', views.orderdetails, name='orderdetails'),
    path ('userorders/',views.useroders,name='userorders'),
    path('vieworderproduct/<int:order_id>/', views.vieworderproduct, name='vieworderproduct'),
    path('cancelorder/<int:order_id>/', views.cancelorder, name='cancelorder'),

]
