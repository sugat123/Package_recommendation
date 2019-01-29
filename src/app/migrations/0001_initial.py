# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-29 02:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('duration', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=100)),
                ('tourtype', models.CharField(max_length=100)),
                ('trekdifficulty', models.CharField(max_length=100)),
                ('operator', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('primary_activity', models.CharField(max_length=100)),
                ('secondary_activity', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('cost_included', models.TextField(blank=True, null=True)),
                ('cost_excluded', models.TextField(blank=True, null=True)),
                ('season', models.CharField(blank=True, max_length=30, null=True)),
                ('like', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
