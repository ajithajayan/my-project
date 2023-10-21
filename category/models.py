from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.text import slugify
from django.urls import reverse
from mptt.models import MPTTModel,TreeForeignKey
# Create your models here.


class Category(MPTTModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('user:product_by_category', args=[self.slug])

    def get_urls(self):
        return reverse('user:filter_product', args=[self.slug])

    def __str__(self):
        if self.parent:
            return f"{self.parent} -> {self.category_name}"
        else:
            return self.category_name
        

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, null=True, blank=True)


    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand_name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.brand_name
        



class Product(models.Model):
    product_id = models.AutoField(primary_key=True ,default=1000)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rprice = models.IntegerField(null=True)

    def __str__(self):
        return self.product_name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('photos/product')

    def __str__(self):
        if self.product:
            return f"Product:{self.product.brand}, {self.product.category}"
        else:
            return "Product: N/A"
        


class VariationManager(models.Manager):
    def colors(self):
        return self.filter(is_active=True).values_list('color', flat=True).distinct()

    def sizes(self):
        return self.filter(is_active=True).values_list('size', flat=True).distinct()

    def variants_by_color(self, color):
        return self.filter(color=color, is_active=True)

    def variants_by_size(self, size):
        return self.filter(size=size, is_active=True)
    


COLOR_CHOICES = [
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('red', 'Red'),
    ('white', 'White'),
]

SIZE_CHOICES = [
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large'),
    ('extra_large', 'Extra Large'),
]



    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, choices=COLOR_CHOICES)
    size = models.CharField(max_length=100, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = VariationManager()
    
    def __str__(self):
        return f"{self.product.product_name} - Color: {self.color}, Size: {self.size}" 


class Offer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"offer"
    


