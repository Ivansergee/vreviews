# Generated by Django 4.0.6 on 2023-07-02 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_alter_suggestion_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='product_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Ссылка на жидкость'),
        ),
    ]
