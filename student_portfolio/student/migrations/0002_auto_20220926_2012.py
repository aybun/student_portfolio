# Generated by Django 3.2 on 2022-09-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='firstname',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='lastname',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='middlename',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='studentId',
            field=models.CharField(blank=True, default='', max_length=11),
        ),
        migrations.AlterField(
            model_name='student',
            name='userId',
            field=models.BigIntegerField(null=True),
        ),
    ]
