# Generated by Django 4.1.2 on 2023-01-09 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('regsiter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cashbacks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('is_cashback', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
                ('shops', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='regsiter.shops')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaveCashback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cashback', models.FloatField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('cashbak_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.cashbacks')),
            ],
        ),
    ]
