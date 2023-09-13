from django.forms import ModelForm
from account.models import Account


class CustomerForm(ModelForm):
    class Meta:
        model=Account  
        fields = ('username', 'email', 'first_name', 'last_name','phone_number', 'password')
