# Generated by Django 4.1.2 on 2023-01-03 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regsiter', '0003_custumusers_promo_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shops',
            name='name_shops',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
