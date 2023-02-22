# Generated by Django 3.2.5 on 2023-02-22 09:27

from django.db import migrations
import private_storage.fields
import private_storage.storage.files
import private_storage_test_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('private_storage_test_app', '0002_auto_20230222_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatemodel',
            name='private_file_1',
            field=private_storage.fields.PrivateFileField(blank=True, max_length=500, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=private_storage_test_app.models.private_test_model_private_file_directory_path),
        ),
        migrations.AlterField(
            model_name='privatemodel',
            name='private_file_2',
            field=private_storage.fields.PrivateFileField(blank=True, max_length=500, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=private_storage_test_app.models.private_test_model_private_file_directory_path),
        ),
    ]
