from haystack import indexes
from .models import Forum


class ForumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    categorys = indexes.CharField(model_attr='category')
    def get_model(self):
        return Forum

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(hidden=False)