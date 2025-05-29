from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('login/',views.loginuser,name='login'),
    path('register/',views.registeruser,name='register'),
    path('userprofile/',views.userprofile,name='userprofile'), 
    path('addshippingaddress/',views.addshippingaddress,name='addshippingaddress'),   
    path('setdefaultshippingaddress/<int:address_id>/',views.setdefaultshippingaddress,name='setdefaultshippingaddress'),     
    path('edituserprofile/',views.edituserprofile,name='edituserprofile'),
    path('editshippingaddress/<int:address_id>',views.editshippingaddress,name='editshippingaddress'),
    path('deleteshippingaddress/<int:address_id>',views.deleteshippingaddress,name='deleteshippingaddress'),
    path('logout/',views.logoutuser, name='logout'),
]
