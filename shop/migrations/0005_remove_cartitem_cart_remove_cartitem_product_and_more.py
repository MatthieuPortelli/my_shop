# Generated by Django 4.1.5 on 2023-01-18 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_cart_product_remove_cart_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
