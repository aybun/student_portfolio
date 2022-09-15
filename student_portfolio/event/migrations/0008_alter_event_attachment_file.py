# Generated by Django 3.2 on 2022-09-15 03:04

from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_alter_event_attachment_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attachment_file',
            field=models.FileField(blank=True, null=True, upload_to=event.models.event_attachment_file_directory_path),
        ),
    ]
