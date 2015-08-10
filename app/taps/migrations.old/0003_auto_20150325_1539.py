# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taps', '0002_tapchange_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tapchange',
            name='user',
            field=models.ForeignKey(related_name='user_changes', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to='users.Profile', null=True, verbose_name='u\u017cytkownik'),
            preserve_default=True,
        ),
    ]
