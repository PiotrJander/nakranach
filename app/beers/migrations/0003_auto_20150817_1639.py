# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from app.main.utils import normalize_for_search


def make_search(apps, schema_editor):
    Beer = apps.get_model("beers", "Beer")
    for beer in Beer.objects.all():
        beer.search = normalize_for_search(beer.brewery.name + ' ' + beer.name)
        beer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0002_beer_search'),
    ]

    operations = [
        migrations.RunPython(make_search),
    ]
