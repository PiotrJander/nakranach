# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0013_auto_20150325_1451'),
        ('users', '0004_profile_favorite_pubs'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=20, verbose_name='Rola', choices=[(b'employee', 'Pracownik baru'), (b'storeman', 'Pracownik magazynu'), (b'admin', 'Administrator')])),
                ('profile', models.ForeignKey(to='users.Profile')),
                ('pub', models.ForeignKey(to='pubs.Pub')),
            ],
            options={
                'verbose_name': 'profil-pub',
                'verbose_name_plural': 'profile-puby',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profile',
            name='pubs',
            field=models.ManyToManyField(related_name='employees', through='users.ProfilePub', to='pubs.Pub'),
            preserve_default=True,
        ),
    ]
