from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'user_side/index.html')

def extend(request):
    return render(request,'user_side/extend.html')