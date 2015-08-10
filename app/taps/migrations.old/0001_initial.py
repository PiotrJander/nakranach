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
            name='TapChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='czas')),
                ('new_beer', models.ForeignKey(related_name='+', editable=False, to='beers.Beer', verbose_name='nowe piwo')),
                ('previous_beer', models.ForeignKey(related_name='+', editable=False, to='beers.Beer', verbose_name='poprzednie piwo')),
                ('tap', models.ForeignKey(editable=False, to='pubs.Tap', verbose_name='tap')),
            ],
            options={
                'verbose_name': 'zmiana na kranie',
                'verbose_name_plural': 'zmiany na kranach',
            },
            bases=(models.Model,),
        ),
    ]
