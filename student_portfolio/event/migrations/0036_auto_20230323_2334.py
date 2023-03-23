# Generated by Django 3.2.5 on 2023-03-23 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0035_alter_curriculum_skillgroups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignskilltoskillgroup',
            name='goal_point',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='skillgroups',
            field=models.ManyToManyField(null=True, related_name='curriculum_skillgroup_set', to='event.Skillgroup'),
        ),
    ]
