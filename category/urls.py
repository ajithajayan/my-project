from django.urls import path,include
from . import views

app_name = 'category'

urlpatterns = [
    
    path('brand-list/', views.brand_list, name='brand-list'),
    path('add-brand/', views.add_brand, name='add_brand'),
    path('edit-brand/<str:brand_name>', views.edit_brand, name='edit_brand'),
    path('delete-brand/<str:brand_name>', views.delete_brand, name='delete_brand'),


    path('category-list/', views.category_list, name='category-list'),
    path('add-category/', views.add_category, name='add-category'),
    path('edit-category/<str:category_name>/', views.edit_category, name='edit-category'),
    path('delete-category/<str:category_name>/', views.delete_category, name='delete-category'),

    path('order_list/', views.order_list, name='order_list'),
    path('ordered_product_details/<int:order_id>', views.ordered_product_details, name='ordered_product_details'),
    path('update_order_status/<str:order_id>/', views.update_order_status, name='update_order_status'),


     path('user_list/', views.user_list, name='user_list'),
     path('block_unblock_user/<int:user_id>/', views.block_unblock_user, name='block_unblock_user'),

     




]