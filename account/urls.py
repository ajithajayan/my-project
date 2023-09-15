from django.urls import path,include
from . import views

app_name = 'account'

urlpatterns = [
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin/logout/',views.admin_logout,name='admin_logout'),
   

    
]