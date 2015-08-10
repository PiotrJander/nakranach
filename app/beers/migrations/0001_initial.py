# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='nazwa')),
                ('ibu', models.IntegerField(null=True, verbose_name='IBU', blank=True)),
                ('abv', models.DecimalField(null=True, verbose_name='ABV', max_digits=3, decimal_places=1, blank=True)),
            ],
            options={
                'verbose_name': 'piwo',
                'verbose_name_plural': 'piwa',
            },
        ),
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='nazwa')),
                ('country', models.CharField(max_length=255, verbose_name='kraj')),
            ],
            options={
                'verbose_name': 'browar',
                'verbose_name_plural': 'browary',
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='nazwa')),
            ],
            options={
                'verbose_name': 'styl',
                'verbose_name_plural': 'style',
            },
        ),
        migrations.AddField(
            model_name='beer',
            name='brewery',
            field=models.ForeignKey(verbose_name='browar', to='beers.Brewery'),
        ),
        migrations.AddField(
            model_name='beer',
            name='style',
            field=models.ForeignKey(verbose_name='styl', to='beers.Style'),
        ),
    ]
