# Generated by Django 2.2.7 on 2020-03-09 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('path', models.FilePathField(max_length=200, path='/usr/src/app/media', recursive=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('dataset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cellbase.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='PhaseDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('path', models.FilePathField(max_length=200, path='/usr/src/app/media', recursive=True)),
                ('background_subtraction', models.BooleanField()),
                ('crop_min', models.FloatField()),
                ('crop_max', models.FloatField()),
                ('raw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cellbase.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='DatasetTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cellbase.Dataset')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cellbase.Tag')),
            ],
            options={
                'unique_together': {('dataset', 'tag')},
            },
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attr_name', models.CharField(max_length=200)),
                ('attr_value', models.CharField(max_length=200)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cellbase.Dataset')),
            ],
            options={
                'unique_together': {('dataset', 'attr_name')},
            },
        ),
    ]
