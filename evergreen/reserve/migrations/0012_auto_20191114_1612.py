# Generated by Django 2.2.7 on 2019-11-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0011_table_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='hour',
            field=models.IntegerField(choices=[(11, '11:00'), (12, '12:00'), (13, '13:00'), (14, '14:00'), (15, '15:00'), (16, '16:00'), (17, '17:00'), (18, '18:00'), (19, '19:00'), (20, '20:00')], verbose_name="Time you'll arrive"),
        ),
    ]
