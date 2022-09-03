# Generated by Django 4.0.6 on 2022-08-26 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_volume_product_short_desc_product_vg_product_volume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='volume',
        ),
        migrations.AddField(
            model_name='product',
            name='volume',
            field=models.ManyToManyField(related_name='products', to='products.volume'),
        ),
    ]