# Generated by Django 4.1.2 on 2022-10-23 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regsiter', '0003_shops_categor_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='distric',
            name='provie_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='regsiter.province'),
        ),
    ]
