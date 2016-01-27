# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pub',
            name='closes',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pub',
            name='opens',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
