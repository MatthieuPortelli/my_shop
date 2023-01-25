# Generated by Django 4.1.5 on 2023-01-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_address_city_alter_address_postalcode_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.AddField(
            model_name='address',
            name='firstname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='lastname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='postalcode',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
