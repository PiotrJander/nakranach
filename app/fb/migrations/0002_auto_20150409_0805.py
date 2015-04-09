# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='page_id',
        ),
        migrations.AddField(
            model_name='page',
            name='page',
            field=models.CharField(default=datetime.datetime(2015, 4, 9, 6, 5, 16, 252466, tzinfo=utc), unique=True, max_length=255),
            preserve_default=False,
        ),
    ]
