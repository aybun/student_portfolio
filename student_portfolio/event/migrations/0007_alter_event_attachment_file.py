# Generated by Django 3.2 on 2022-09-14 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_auto_20220912_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attachment_file',
            field=models.FileField(blank=True, null=True, upload_to='events'),
        ),
    ]
