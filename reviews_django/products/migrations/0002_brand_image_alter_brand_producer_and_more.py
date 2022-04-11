# Generated by Django 4.0.3 on 2022-04-09 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(default='placeholder.jpg', upload_to='brands/'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='brands', to='products.producer'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='flavors',
            field=models.ManyToManyField(related_name='products', to='products.flavor'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='placeholder.jpg', upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='comments',
            field=models.ManyToManyField(related_name='reviews', to='products.comment'),
        ),
    ]