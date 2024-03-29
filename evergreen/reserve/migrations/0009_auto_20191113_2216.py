# Generated by Django 2.2.7 on 2019-11-14 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0008_remove_table_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('min_person', models.IntegerField()),
                ('max_person', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='table',
            name='max_person',
        ),
        migrations.RemoveField(
            model_name='table',
            name='min_person',
        ),
        migrations.AlterField(
            model_name='table',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
