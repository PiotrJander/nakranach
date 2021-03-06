# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0001_initial'),
        ('users', '0001_initial'),
        ('pubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TapChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='czas')),
                ('new_beer', models.ForeignKey(related_name='+', blank=True, editable=False, to='beers.Beer', null=True, verbose_name='nowe piwo')),
                ('previous_beer', models.ForeignKey(related_name='+', blank=True, editable=False, to='beers.Beer', null=True, verbose_name='poprzednie piwo')),
                ('tap', models.ForeignKey(editable=False, to='pubs.Tap', verbose_name='tap')),
                ('user', models.ForeignKey(related_name='user_changes', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to='users.Profile', null=True, verbose_name='u\u017cytkownik')),
            ],
            options={
                'verbose_name': 'zmiana na kranie',
                'verbose_name_plural': 'zmiany na kranach',
            },
        ),
    ]
