# Generated by Django 4.0.6 on 2023-05-05 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_brand_created_at_producer_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='vg',
            field=models.IntegerField(default=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='nic_content',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.nicotine'),
        ),
        migrations.AddField(
            model_name='product',
            name='volume',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.volume'),
        ),
    ]