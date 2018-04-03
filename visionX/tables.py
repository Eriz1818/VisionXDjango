import django_tables2 as tables
from .models import TagFreq
from .models import TempTable


class TagFreqTable(tables.Table):
    class Meta:
        model = TagFreq
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}

class TempTagFreqTable(tables.Table):
    class Meta:
        model = TempTable
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        fields = ('TempTagName', 'TempTagFreq')
