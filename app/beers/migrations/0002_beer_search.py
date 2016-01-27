# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='search',
            field=models.CharField(default='', max_length=511, editable=False),
            preserve_default=False,
        ),
    ]
