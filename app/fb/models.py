from django.db import models

from app.pubs.models import Pub

class Page(models.Model):
    page_id = models.CharField(max_length=255)
    pub = models.ForeignKey(Pub)
