from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables


class TapTable(tables.Table):
    tap = tables.Column(accessor='description', verbose_name=_('Kran'))
    brewery = tables.Column(accessor='beer.brewery.name', verbose_name=_('Browar'))
    beer_name = tables.Column(accessor='beer.name', verbose_name=_('Piwo'))
    actions = tables.TemplateColumn(accessor='id', verbose_name=_('Akcje'), template_name='taps/_change_beer_form.html')

    class Meta:
        attrs = {'class': 'table', 'data-sortable': 'data-sortable', }
        orderable = False