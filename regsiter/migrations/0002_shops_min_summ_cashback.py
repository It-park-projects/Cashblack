# Generated by Django 4.1.2 on 2023-01-08 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regsiter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shops',
            name='min_summ_cashback',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
