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
            name='latitude',
            field=models.DecimalField(editable=False, max_digits=6, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pub',
            name='longitude',
            field=models.DecimalField(editable=False, max_digits=6, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pub',
            name='slug',
            field=models.CharField(max_length=200, editable=False),
            preserve_default=True,
        ),
    ]
