# Generated by Django 4.1.2 on 2022-10-27 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regsiter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='custumusers',
            name='barcode',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='custumusers',
            name='barcode_id',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
