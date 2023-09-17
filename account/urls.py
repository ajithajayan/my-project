from django.urls import path,include
from . import views

app_name = 'account'

urlpatterns = [
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin/logout/',views.admin_logout,name='admin_logout'),
    
    path('index',views.index,name='index'),
    path('user-login/',views.user_login,name='user-login'),
    path('user-signup/',views.user_signup,name='user-signup'),
    path('user-logout',views.user_logout,name='user-logout'),
    
]