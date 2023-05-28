# Generated by Django 4.0.6 on 2023-05-25 16:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0021_alter_product_brand_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.brand'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='flavors',
            field=models.ManyToManyField(related_name='products', to='products.flavor'),
        ),
        migrations.AlterField(
            model_name='product',
            name='nic_content',
            field=models.ManyToManyField(related_name='products', to='products.nicotine'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='vg',
            field=models.IntegerField(default=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='volume',
            field=models.ManyToManyField(related_name='products', to='products.volume'),
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('comment', models.TextField(blank=True, null=True)),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('text', models.TextField(blank=True, default='', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestion', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]