# Generated by Django 3.2.5 on 2023-03-25 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_alter_userprofile_enroll'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]
