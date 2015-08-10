# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0003_beer'),
        ('pubs', '0013_auto_20150325_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub',
            name='waiting_beers',
            field=models.ManyToManyField(related_name='waiting_in_pubs', through='pubs.WaitingBeer', to='beers.Beer'),
            preserve_default=True,
        ),
    ]
