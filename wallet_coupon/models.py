from django.db import models
from account.models import *
from category.models import *
from django.utils import timezone

class Wallet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=100)
    referral_id = models.CharField(max_length=20, unique=True, null=True,blank=True)
    referrer = models.ForeignKey(Account, related_name='referrals', null=True, on_delete=models.SET_NULL,blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super().save(*args, **kwargs)


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_amount = models.IntegerField(default=1000)
    valid_from = models.DateField()
    valid_to = models.DateField()


    def is_redeemed_by_user(self, user):
        redeemed_details = Coupon_Redeemed_Details.objects.filter(coupon=self, user=user, is_redeemed=True)
        return redeemed_details.exists()


class Coupon_Redeemed_Details(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_redeemed = models.BooleanField(default=False)


class WishList(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	date_added = models.DateField(default=timezone.now)


