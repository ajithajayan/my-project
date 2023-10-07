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
    path('sent-otp',views.sent_otp,name='sent-otp'),
    path('verify-otp',views.verify_otp,name='verify-otp'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/forgot_password',views.verify_otp_forgot_password,name='verify-otp-forgot-password'),
    path('sent-otp/forgot_password',views.sent_otp_forgot_password,name='sent-otp-forgot-password'),

   
]