# Generated by Django 3.2.5 on 2023-02-23 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0030_alter_curriculum_skillgroups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='skillgroups',
            field=models.ManyToManyField(null=True, related_name='curriculum_skillgroup_set', to='event.Skillgroup'),
        ),
    ]
