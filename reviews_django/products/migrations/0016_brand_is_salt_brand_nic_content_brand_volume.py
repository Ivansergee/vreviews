# Generated by Django 4.0.6 on 2022-10-11 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_producer_ig_producer_tg_producer_vk_producer_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='is_salt',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='nic_content',
            field=models.ManyToManyField(blank=True, null=True, related_name='brands', to='products.nicotine'),
        ),
        migrations.AddField(
            model_name='brand',
            name='volume',
            field=models.ManyToManyField(blank=True, null=True, related_name='brands', to='products.volume'),
        ),
    ]
