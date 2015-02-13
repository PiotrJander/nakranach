# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0003_beer'),
        ('pubs', '0003_auto_20150202_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='tap',
            name='beer',
            field=models.ForeignKey(related_name='taps', blank=True, to='beers.Beer', null=True),
            preserve_default=True,
        ),
    ]
