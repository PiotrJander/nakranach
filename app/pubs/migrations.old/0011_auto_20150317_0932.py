# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0010_auto_20150317_0927'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tap',
            options={'ordering': ('sort_order',)},
        ),
        migrations.RenameField(
            model_name='tap',
            old_name='order',
            new_name='sort_order',
        ),
        migrations.AlterUniqueTogether(
            name='tap',
            unique_together=set([('pub', 'sort_order')]),
        ),
    ]
