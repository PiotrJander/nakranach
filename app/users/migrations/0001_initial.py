# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'adres email')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar_url', models.URLField(max_length=1000, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('surname', models.CharField(max_length=255, null=True, blank=True)),
                ('favorite_pubs', models.ManyToManyField(to='pubs.Pub', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=20, verbose_name='Rola', choices=[(b'employee', 'Pracownik baru'), (b'storeman', 'Pracownik magazynu'), (b'admin', 'Administrator')])),
                ('profile', models.ForeignKey(verbose_name='U\u017cytkownik', to='users.Profile')),
                ('pub', models.ForeignKey(verbose_name='Pub', to='pubs.Pub')),
            ],
            options={
                'verbose_name': 'profil-pub',
                'verbose_name_plural': 'profile-puby',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='pubs',
            field=models.ManyToManyField(related_name='employees', through='users.ProfilePub', to='pubs.Pub'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='profilepub',
            unique_together=set([('profile', 'pub')]),
        ),
    ]
