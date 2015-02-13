# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0003_beer'),
        ('pubs', '0003_auto_20150202_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingBeer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beer', models.ForeignKey(to='beers.Beer')),
                ('pub', models.ForeignKey(to='pubs.Pub')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
