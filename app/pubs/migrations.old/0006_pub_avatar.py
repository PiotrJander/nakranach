# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'uploads/pubs', blank=True),
            preserve_default=True,
        ),
    ]
