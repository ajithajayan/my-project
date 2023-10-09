from django import forms
from category.models import Product,ProductVariant,COLOR_CHOICES,SIZE_CHOICES

class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [ 'product_name', 'category', 'brand', 'description', 'price', 'image']


class AddVariantForm(forms.ModelForm):
    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    size = forms.ChoiceField(choices=SIZE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model=ProductVariant
        fields=['product','color','size','stock','is_active']