# Generated by Django 3.2.8 on 2021-10-30 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_cart_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
    ]
