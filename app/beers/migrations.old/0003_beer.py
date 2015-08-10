# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0002_auto_20150205_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='nazwa')),
                ('ibu', models.IntegerField(null=True, verbose_name='IBU', blank=True)),
                ('abv', models.DecimalField(null=True, verbose_name='ABV', max_digits=3, decimal_places=1, blank=True)),
                ('brewery', models.ForeignKey(verbose_name='browar', to='beers.Brewery')),
                ('style', models.ForeignKey(verbose_name='styl', to='beers.Style')),
            ],
            options={
                'verbose_name': 'piwo',
                'verbose_name_plural': 'piwa',
            },
            bases=(models.Model,),
        ),
    ]
