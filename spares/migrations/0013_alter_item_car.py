# Generated by Django 3.2.3 on 2021-07-01 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_car_car_model'),
        ('spares', '0012_alter_item_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Car', to='cars.car'),
        ),
    ]