# Generated by Django 4.0.6 on 2022-07-24 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_product_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='No description'),
            preserve_default=False,
        ),
    ]