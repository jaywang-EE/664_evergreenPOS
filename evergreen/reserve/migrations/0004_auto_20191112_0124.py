# Generated by Django 2.2.7 on 2019-11-12 06:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0003_auto_20191111_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='hour',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)]),
        ),
    ]
