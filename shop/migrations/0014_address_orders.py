# Generated by Django 4.1.5 on 2023-01-21 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_remove_address_user_address_firstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='orders',
            field=models.ManyToManyField(to='shop.order'),
        ),
    ]
