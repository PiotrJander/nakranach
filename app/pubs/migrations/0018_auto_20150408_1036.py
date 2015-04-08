# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='beer',
            field=models.ForeignKey(related_name='prices', blank=True, to='pubs.WaitingBeer', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='price',
            name='tap',
            field=models.ForeignKey(related_name='prices', blank=True, to='pubs.Tap', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pub',
            name='avatar',
            field=models.ImageField(help_text='Preferred size is 256x256. If uploaded image has different size, it will be resized automatically', null=True, upload_to=b'pubs', blank=True),
            preserve_default=True,
        ),
    ]
