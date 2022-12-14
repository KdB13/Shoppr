# Generated by Django 4.0.6 on 2022-07-23 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField(default=0)),
                ('photo', models.ImageField(upload_to='products')),
            ],
        ),
    ]
