# Generated by Django 4.0.6 on 2022-08-24 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_avg_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='review_count',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='score_count',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
