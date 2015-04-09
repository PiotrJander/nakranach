from django.db import models

from app.pubs.models import Pub

class Page(models.Model):
    page = models.CharField(max_length=255, unique=True)
    pub = models.ForeignKey(Pub)
