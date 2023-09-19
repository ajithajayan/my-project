from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.text import slugify
from pyotp import TOTP

# Create your models here.


class MyAccountManager(BaseUserManager):

    def create_user(self,username,email,phone_number,password=None):
        
        if not email:
            raise ValueError('you must have an email')
        if not username:
            raise ValueError('user must have a username')
        user=self.model(
            email=self.normalize_email(email),# this will neglect the casesensitive
            username=username,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self.db)
        return user
    
    #creating coustom superuser

    def create_superuser(self,username,email,password,phone_number):
        user=self.create_user(
            email=self.normalize_email(email),# this will neglect the casesensitive
            username=username,
            password=password,
            phone_number=phone_number

        )

        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self.db)
        return user


class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50,null=True,blank=True)
    last_name=models.CharField(max_length=50,null=True,blank=True)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=50)

    #requierd

    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','phone_number']
    objects=MyAccountManager()

    def __str__(self):
        return self.email     
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_labal):
        return True 
    






class AdressBook(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50,blank=True,null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)        




class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=16)  # Store the OTP secret key
