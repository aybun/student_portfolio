# Generated by Django 3.2.5 on 2023-02-22 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import private_storage.fields
import private_storage.storage.files
import private_storage_test_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('private_file_1', private_storage.fields.PrivateFileField(storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=private_storage_test_app.models.private_test_model_private_file_directory_path)),
                ('private_file_2', private_storage.fields.PrivateFileField(storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=private_storage_test_app.models.private_test_model_private_file_directory_path)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='privatemodel_created_by_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
