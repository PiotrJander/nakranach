# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0011_auto_20150317_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub',
            name='closes',
            field=models.TimeField(default=datetime.datetime(2015, 3, 17, 8, 55, 31, 551760, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pub',
            name='opens',
            field=models.TimeField(default=datetime.datetime(2015, 3, 17, 8, 55, 37, 119465, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
