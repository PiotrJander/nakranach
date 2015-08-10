# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0012_auto_20150317_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pub',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pub',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True),
            preserve_default=True,
        ),
    ]
