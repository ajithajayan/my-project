# Generated by Django 4.2.5 on 2023-10-11 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_coupon', '0003_coupon_coupon_redeemed_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='minimum_amount',
            field=models.IntegerField(default=1000),
        ),
    ]