# Generated by Django 4.0.3 on 2022-04-22 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_reaction_remove_reviewreaction_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL),
        ),
    ]