# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150325_1538'),
        ('taps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tapchange',
            name='user',
            field=models.ForeignKey(related_name='user_changes', on_delete=django.db.models.deletion.SET_NULL, verbose_name='u\u017cytkownik', blank=True, to='users.Profile', null=True),
            preserve_default=True,
        ),
    ]
