# Generated by Django 4.2.5 on 2023-10-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_account_referral_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(blank=True, default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(blank=True, default=1, max_length=50),
            preserve_default=False,
        ),
    ]
