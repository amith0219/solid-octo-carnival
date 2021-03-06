# Generated by Django 2.2.12 on 2020-07-09 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='details',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
