# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0001_initial'),
    ]

    operations = [
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
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='brewery',
            options={'verbose_name': 'browar', 'verbose_name_plural': 'browary'},
        ),
    ]
