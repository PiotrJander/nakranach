from haystack import indexes

from .models import Pub

class PubIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Pub