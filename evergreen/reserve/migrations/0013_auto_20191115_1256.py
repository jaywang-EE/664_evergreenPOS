# Generated by Django 2.2.7 on 2019-11-15 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0012_auto_20191114_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='person',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Number of diners'),
        ),
    ]