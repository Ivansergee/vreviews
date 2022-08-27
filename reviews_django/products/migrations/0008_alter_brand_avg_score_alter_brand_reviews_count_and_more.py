# Generated by Django 4.0.6 on 2022-08-26 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_brand_avg_score_brand_reviews_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='avg_score',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='reviews_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='score_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='avg_score',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='reviews_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='score_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='avg_score',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='reviews_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='score_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
