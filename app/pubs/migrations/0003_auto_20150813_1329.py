# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0002_auto_20150813_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pub',
            name='avatar',
            field=models.ImageField(default='', help_text='Preferred size is 256x256. If uploaded image has different size, it will be resized automatically', upload_to=b'pubs', blank=True),
            preserve_default=False,
        ),
    ]
