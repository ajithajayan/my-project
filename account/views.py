from django.shortcuts import render
from .forms import CustomerForm

# Create your views here.
app_name='account'

def index(request):
    form=CustomerForm()
    context={'form':form}
    return render(request,'user_side/extend.html',context)
