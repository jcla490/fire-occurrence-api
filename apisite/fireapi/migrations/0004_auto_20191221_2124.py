# Generated by Django 2.2.5 on 2019-12-21 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireapi', '0003_auto_20191221_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fires',
            name='country',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='fires',
            name='source',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='fires',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='fires',
            name='state',
            field=models.CharField(max_length=200),
        ),
    ]
