from django.urls import path,include
from . import views

app_name = 'cart'

urlpatterns = [

    path('shoping_cart/', views.cart, name='shopping_cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('add_quantity_to_cart/<int:product_id>/<int:cart_item_id>/', views.add_quantity_to_cart, name='add_quantity_to_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    

    path('api/get_cart_count/', views.get_cart_count, name='get_cart_count'),
   
]