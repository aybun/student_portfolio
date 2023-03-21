# Generated by Django 3.2.5 on 2023-03-21 07:42

from django.db import migrations, models
import event.models
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0032_auto_20230223_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='attachment_file',
            field=private_storage.fields.PrivateFileField(blank=True, max_length=500, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=event.models.curriculum_attachment_file_directory_path),
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='skillgroups',
            field=models.ManyToManyField(null=True, related_name='curriculum_skillgroup_set', to='event.Skillgroup'),
        ),
    ]
