# Generated by Django 4.0.6 on 2022-07-29 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_remove_profile_mail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='gender',
        ),
    ]
