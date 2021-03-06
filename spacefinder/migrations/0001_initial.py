# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 15:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=200)),
                ('department_icon', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=3)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('karma', models.IntegerField(default=0)),
                ('rating_streak', models.IntegerField(default=0)),
                ('avatar', models.ImageField(default='user_avatars/default.png', upload_to='user_avatars')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spacefinder.Department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudySpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('space_name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('wheelchair_access', models.BooleanField(default=False)),
                ('computer_access', models.BooleanField(default=False)),
                ('avg_rating', models.FloatField(default=3.0)),
                ('opening_time', models.TimeField(default='06:00:00')),
                ('closing_time', models.TimeField(default='18:00:00')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spacefinder.Department')),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spacefinder.Student'),
        ),
        migrations.AddField(
            model_name='rating',
            name='studyspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spacefinder.StudySpace'),
        ),
    ]
