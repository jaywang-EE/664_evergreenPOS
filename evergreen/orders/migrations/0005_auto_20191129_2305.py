# Generated by Django 2.2.7 on 2019-11-30 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20191117_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='addr',
            field=models.CharField(default='7643225555', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='15456', max_length=12),
            preserve_default=False,
        ),
    ]
