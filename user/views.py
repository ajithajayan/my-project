from django.shortcuts import render,redirect
from account.forms import CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def index(request):
    return render(request,'user_side/index.html')

def extend(request):
    return render(request,'user_side/extend.html')


def signuppage (request):
    if request.user.is_authenticated:
        return redirect('user:home')
    form = CustomerForm()
    context = {'form':form}
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if form.is_valid():
            if password != confirm_password:
                messages.error(request, "Password Not Match")
                return render(request, 'user_side/user-signup.html', {'form': form})
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data["password"]
            )
            messages.success(request, "Account Created Succesfuly , Please Activate to Continue")
            return redirect('user:login-page')
        else:
            return render(request, 'user_side/user-signup.html', {'form': form})
    else:
        form = CustomerForm()
    
    
    
    return render(request, 'user_side/user-signup.html')