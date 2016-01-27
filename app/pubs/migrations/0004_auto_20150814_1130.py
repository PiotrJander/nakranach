# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0003_auto_20150813_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitingbeer',
            name='_brewery',
            field=models.CharField(default='', max_length=255, verbose_name='browar', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='waitingbeer',
            name='_style',
            field=models.CharField(default='', max_length=255, verbose_name='styl', blank=True),
            preserve_default=False,
        ),
    ]
