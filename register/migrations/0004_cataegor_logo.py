# Generated by Django 4.1.2 on 2022-10-21 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_cataegor_create_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cataegor',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logo_categor/'),
        ),
    ]
