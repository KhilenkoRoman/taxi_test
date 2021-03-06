# Generated by Django 3.0.3 on 2020-02-18 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=32, verbose_name='model')),
                ('car_number', models.CharField(max_length=16, verbose_name='car number')),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('phone_number', models.CharField(max_length=16)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], max_length=8)),
                ('order_address', models.TextField()),
                ('target_address', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='core.Car')),
            ],
        ),
    ]
