# Generated by Django 4.1.2 on 2023-01-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_balans_last_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balans',
            name='last_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
