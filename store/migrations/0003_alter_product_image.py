# Generated by Django 3.2.9 on 2021-11-28 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(max_length=200),
        ),
    ]
