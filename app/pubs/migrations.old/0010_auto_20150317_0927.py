# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0009_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tap',
            options={},
        ),
        migrations.RemoveField(
            model_name='tap',
            name='sort_order',
        ),
        migrations.AddField(
            model_name='tap',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pub',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'pubs', blank=True),
            preserve_default=True,
        ),
    ]
