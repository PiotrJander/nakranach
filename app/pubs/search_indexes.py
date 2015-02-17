from haystack import indexes

from .models import Pub

class PubIndex(indexes.ModelSearchIndex, indexes.Indexable):
    content_auto = indexes.EdgeNgramField()

    class Meta:
        model = Pub
        fields = ['name', 'city', 'address']

    def prepare_content_auto(self, object):
        return '%s, %s, %s' % (object.name, object.city, object.address)