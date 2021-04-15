# Generated by Django 3.1.7 on 2021-04-15 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('min_iteration3', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute_selection',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='attribute_selection',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='desired_partner',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='group_former',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='projects',
        ),
        migrations.RemoveField(
            model_name='project',
            name='group_former',
        ),
        migrations.RemoveField(
            model_name='project_selection',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='project_selection',
            name='project',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='attribute_selection',
        ),
        migrations.DeleteModel(
            name='GroupFormer',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='project_selection',
        ),
    ]
