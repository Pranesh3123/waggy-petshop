from django.urls import path
from . import views

urlpatterns = [
    path('',views.recommended_and_bestselling_products, name='recommendedandbestsellingproducts'),
    path('shop/',views.shop,name='shop'),
    path('viewproduct/<str:product_id>/',views.viewproduct,name='viewproduct'),

]
