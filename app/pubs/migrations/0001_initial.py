# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Pub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nazwa')),
                ('slug', models.CharField(max_length=200, editable=False)),
                ('city', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=250, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('avatar', models.ImageField(help_text='Preferred size is 256x256. If uploaded image has different size, it will be resized automatically', null=True, upload_to=b'pubs', blank=True)),
                ('avatar_timestamp', models.DateTimeField(auto_now_add=True)),
                ('opens', models.TimeField()),
                ('closes', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('type', models.CharField(default=b'tap', max_length=32, verbose_name='Rodzaj kranu', choices=[(b'pump', 'Pompa'), (b'tap', 'Kran')])),
                ('beer', models.ForeignKey(related_name='taps', blank=True, to='beers.Beer', null=True)),
                ('pub', models.ForeignKey(related_name='taps', to='pubs.Pub')),
            ],
            options={
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.PositiveIntegerField(help_text='W ml', verbose_name='Obj\u0119to\u015b\u0107')),
                ('pub', models.ForeignKey(related_name='available_volumes', to='pubs.Pub')),
            ],
        ),
        migrations.CreateModel(
            name='WaitingBeer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_name', models.CharField(max_length=255, verbose_name='nazwa', blank=True)),
                ('_ibu', models.IntegerField(null=True, verbose_name='IBU', blank=True)),
                ('_abv', models.DecimalField(null=True, verbose_name='ABV', max_digits=3, decimal_places=1, blank=True)),
                ('_brewery', models.ForeignKey(verbose_name='browar', blank=True, to='beers.Brewery', null=True)),
                ('_style', models.ForeignKey(verbose_name='styl', blank=True, to='beers.Style', null=True)),
                ('beer', models.ForeignKey(to='beers.Beer')),
                ('pub', models.ForeignKey(to='pubs.Pub')),
            ],
        ),
        migrations.AddField(
            model_name='pub',
            name='waiting_beers',
            field=models.ManyToManyField(related_name='waiting_in_pubs', through='pubs.WaitingBeer', to='beers.Beer'),
        ),
        migrations.AddField(
            model_name='price',
            name='beer',
            field=models.ForeignKey(related_name='prices', blank=True, to='pubs.WaitingBeer', null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='tap',
            field=models.ForeignKey(related_name='prices', blank=True, to='pubs.Tap', null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='volume',
            field=models.ForeignKey(related_name='prices', to='pubs.Volume'),
        ),
        migrations.AlterUniqueTogether(
            name='tap',
            unique_together=set([('pub', 'sort_order')]),
        ),
    ]
