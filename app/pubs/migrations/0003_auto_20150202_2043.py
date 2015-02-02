# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0002_auto_20150202_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pub',
            name='latitude',
            field=models.DecimalField(null=True, editable=False, max_digits=6, decimal_places=3, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pub',
            name='longitude',
            field=models.DecimalField(null=True, editable=False, max_digits=6, decimal_places=3, blank=True),
            preserve_default=True,
        ),
    ]
