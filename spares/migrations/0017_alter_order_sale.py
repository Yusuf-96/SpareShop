# Generated by Django 3.2.3 on 2021-07-07 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0016_alter_sale_sales_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='sale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='spares.sale'),
        ),
    ]
