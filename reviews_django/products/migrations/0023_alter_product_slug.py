# Generated by Django 4.0.6 on 2023-05-29 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_product_brand_alter_product_flavors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default=None, null=True, unique=True),
        ),
    ]