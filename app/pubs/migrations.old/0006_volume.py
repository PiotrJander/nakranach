# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0005_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.PositiveIntegerField(help_text='W ml', verbose_name='Obj\u0119to\u015b\u0107')),
                ('pub', models.ForeignKey(related_name='available_volumes', to='pubs.Pub')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
