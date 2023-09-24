from django.urls import path,include
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index,name='index'),
    path('product-detail/<int:product_id>/', views.product_detail, name='product-detail'),
    
    
]
