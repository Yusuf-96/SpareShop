# Generated by Django 3.2.3 on 2021-06-27 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0003_alter_item_car'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-ordered_date',)},
        ),
    ]
