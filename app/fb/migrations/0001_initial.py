# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0014_pub_waiting_beers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_id', models.CharField(max_length=255)),
                ('pub', models.ForeignKey(to='pubs.Pub')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
