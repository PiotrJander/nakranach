# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0015_pub_avatar_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pub',
            name='avatar_timestamp',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
