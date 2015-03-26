# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taps', '0003_auto_20150325_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tapchange',
            name='new_beer',
            field=models.ForeignKey(related_name='+', blank=True, editable=False, to='beers.Beer', null=True, verbose_name='nowe piwo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tapchange',
            name='previous_beer',
            field=models.ForeignKey(related_name='+', blank=True, editable=False, to='beers.Beer', null=True, verbose_name='poprzednie piwo'),
            preserve_default=True,
        ),
    ]
