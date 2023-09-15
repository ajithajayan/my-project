from django.forms import ModelForm
from account.models import Account


class CustomerForm(ModelForm):
    class Meta:
        model=Account  
        fields = ( 'email', 'password')
