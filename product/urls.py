from django.urls import path,include
from . import views

app_name = 'product'

urlpatterns = [

    path('product-list/', views.product_list, name='product-list'),
    path('add-product/', views.add_product, name='add-product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('soft_delete_product/<int:product_id>/', views.soft_delete_product, name='soft_delete_product'),
    
    
]