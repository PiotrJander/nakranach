# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0006_volume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tap', models.ForeignKey(related_name='prices', to='pubs.Tap')),
                ('volume', models.ForeignKey(related_name='prices', to='pubs.Volume')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
