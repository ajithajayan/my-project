from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CustomerForm
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.urls import reverse  # Import the reverse function

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
            messages.error(request, "You are blocked by admin ! Please contact admin")
            return redirect('account:user-login') 
        
        user = authenticate(email=email,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('account:user-login')
        else:
            login(request,user)
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
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        confirm_password = request.POST.get('confirm_password')
        referral_code = request.POST.get('ref_code')

        if  Account.objects.filter(email=email).exists():
            messages.error(request, "Email Adress already existing")
            return redirect('account:user-signup')
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('account:user-signup')
        user=Account.objects.create(email=email, password=password,username=user, phone_number=mobile)
        user.save()
        return redirect('account:user-login')
    
    return render(request,'user_side/user_signup.html')


def user_logout(request):
    logout(request)
    return redirect('account:index')

def index(request):

    return render(request,'user_side/index.html')