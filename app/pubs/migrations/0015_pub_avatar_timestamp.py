# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0014_pub_waiting_beers'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub',
            name='avatar_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 2, 11, 25, 17, 143102, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
