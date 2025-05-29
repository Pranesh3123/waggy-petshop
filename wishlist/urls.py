from django.urls import path
from . import views

urlpatterns = [
    path('wishlist/',views.wishlist,name='wishlist'),
    path('addwishproduct/<str:product_id>',views.addwishproduct,name='addwishproduct'),
    path('removewishproduct/<int:item_id>/', views.removewishproduct, name='removewishproduct'),
    path('wishlistcount/', views.wishlistcount, name='wishlistcount'),

]
