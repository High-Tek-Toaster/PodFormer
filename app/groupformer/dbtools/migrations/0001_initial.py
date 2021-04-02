# Generated by Django 3.1.7 on 2021-04-01 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attr_name', models.CharField(max_length=100)),
                ('is_homogenous', models.BooleanField()),
                ('is_continuous', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='attribute_selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbtools.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='GroupFormer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prof_name', models.CharField(max_length=200)),
                ('prof_email', models.CharField(max_length=200)),
                ('class_section', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_email', models.CharField(max_length=200)),
                ('part_name', models.CharField(max_length=200)),
                ('attributes', models.ManyToManyField(through='dbtools.attribute_selection', to='dbtools.Attribute')),
                ('desired_partner', models.ManyToManyField(blank=True, to='dbtools.Participant')),
                ('group_former', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbtools.groupformer')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('project_description', models.CharField(max_length=1000)),
                ('group_former', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbtools.groupformer')),
            ],
        ),
        migrations.CreateModel(
            name='project_selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbtools.participant')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbtools.project')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='projects',
            field=models.ManyToManyField(through='dbtools.project_selection', to='dbtools.Project'),
        ),
        migrations.AddField(
            model_name='attribute_selection',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbtools.participant'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='group_former',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbtools.groupformer'),
        ),
    ]
