# Generated by Django 4.0.5 on 2022-07-09 23:10

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_profile_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default_avatar.png', upload_to=products.models.Profile.image_path),
        ),
    ]
