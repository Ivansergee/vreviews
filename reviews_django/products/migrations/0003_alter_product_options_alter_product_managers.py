# Generated by Django 4.0.3 on 2022-04-17 12:15

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_brand_image_alter_brand_producer_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'default_manager_name': 'published_objects', 'ordering': ['-created_at']},
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('published_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]