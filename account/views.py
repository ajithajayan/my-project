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
