from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = list_display = ('product', 'variation_category', 'variation_value', 'is_active')

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name',)}
    list_display = ('brand_name', 'slug')

# this will register the class to the site


admin.site.register(Product)
admin.site.register(ProductImage) 
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Offer)