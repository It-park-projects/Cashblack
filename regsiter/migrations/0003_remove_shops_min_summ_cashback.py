# Generated by Django 4.1.2 on 2023-01-08 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regsiter', '0002_shops_min_summ_cashback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shops',
            name='min_summ_cashback',
        ),
    ]
