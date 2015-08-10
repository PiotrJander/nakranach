# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Nazwa')),
                ('slug', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=250, blank=True)),
                ('latitude', models.DecimalField(max_digits=6, decimal_places=3)),
                ('longitude', models.DecimalField(max_digits=6, decimal_places=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(db_index=True, blank=True)),
                ('type', models.CharField(default=b'tap', max_length=32, verbose_name='Rodzaj kranu', choices=[(b'pump', b'Pompa'), (b'tap', b'Kran')])),
                ('pub', models.ForeignKey(related_name='taps', to='pubs.Pub')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
