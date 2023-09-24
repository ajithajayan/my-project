from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CustomerForm
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.urls import reverse  # Import the reverse function
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
import random
from category.models import *
# ------------------------------------------#forgot password#------------------------------

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('account:admin_dashboard')

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_superadmin:
                login(request, user)
                messages.success(request, "Admin login successful!")
                return redirect('account:admin_dashboard')  # Use the named URL pattern
            messages.error(request, "Invalid admin credentials!")


    return render(request, 'admin_side/authentication-login.html')


@login_required(login_url='account:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    return render(request, 'admin_side/index.html')

def admin_logout(request):
    logout(request)
    return redirect('account:admin_login')  



# <---------------------------------------------------------user-login-------------------------------------------------------->


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('account:index')
    
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)

        if not Account.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email Adress")
            return redirect('account:user-login')
        
        if not Account.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "You are blocked by admin ! Please contact admin ")
            return redirect('account:user-login') 
        
        user = authenticate(email=email,password=password)
        print(user)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('account:user-login')
        else:
            login(request,user)
            messages.success(request, "signup successful!")
            return redirect('account:index')
    
    return render(request,'user_side/user_signin.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('account:index')
    if request.method=='POST':
        user=request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        confirm_password = request.POST.get('confirm_password')
        referral_code = request.POST.get('ref_code')

        if  Account.objects.filter(email=email).exists():
            messages.error(request, "Email Adress already existing")
            return redirect('account:user-signup')
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('account:user-signup')
        user=Account.objects.create_user(email=email, password=password,username=user, phone_number=mobile)
        user.save()
        request.session['email']=email
        return redirect('account:sent-otp')
    
    return render(request,'user_side/user_signup.html')


def user_logout(request):
    logout(request)
    messages.success(request, "logout successful!")
    return redirect('account:index')

def index(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'user_side/index.html',context)


def sent_otp(request):
   random_num=random.randint(1000,9999)
   request.session['OTP_Key']=random_num
   send_mail(
   "OTP AUTHENTICATING fKart",
   f"{random_num} -OTP",
   "ajithajayan222aa@gmail.com",
   [request.session['email']],
   fail_silently=False,
    )
   return redirect('account:verify-otp')


def verify_otp(request):
   user=Account.objects.get(email=request.session['email'])
   if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         print(request.session['OTP_Key'],request.POST['otp'])
         user.is_active=False
      else:
         login(request,user)
         messages.success(request, "signup successful!")
         return redirect('account:index')
   return render(request,'user_side/verify_otp.html')


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         if Account.objects.filter(email=email).exists():
#             user = Account.objects.get(email__exact=email)
            
            
#             #SEND FORGOT PASSWORD MAIL
#             current_site = get_current_site(request)
#             mail_subject = 'Reset Your Password'
#             message = render_to_string ('accounts/reset_password_email.html',{
#                 'user' : user,
#                 'domain' : current_site,
#                 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token' : default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject,message,to=[to_email])
#             send_email.content_subtype = 'html'
#             send_email.send()
#             messages.success(request, "Email Has Been Successfully shared , please verify to reset")
#             return redirect('account:user-login')
#         else:
            
#             messages.error(request, "Account Not Exists , Please Sign Up")

            
#     return render(request, 'user_side/forgot-password.html')


