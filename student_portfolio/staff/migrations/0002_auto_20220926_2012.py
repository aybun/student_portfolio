# Generated by Django 3.2 on 2022-09-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='userId',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staffId',
            field=models.CharField(default='', max_length=11),
        ),
    ]
