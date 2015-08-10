# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150325_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepub',
            name='profile',
            field=models.ForeignKey(verbose_name='U\u017cytkownik', to='users.Profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profilepub',
            name='pub',
            field=models.ForeignKey(verbose_name='Pub', to='pubs.Pub'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='profilepub',
            unique_together=set([('profile', 'pub')]),
        ),
    ]
