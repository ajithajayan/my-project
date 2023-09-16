from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
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
    # stock = models.IntegerField(default=0)
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
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    



variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
) 



class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    


class Offer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"offer"
    
