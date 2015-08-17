import django_tables2 as tables


class WaitingBeersTable(tables.Table):
    brewery = tables.Column(verbose_name='Browar')
    name = tables.Column(verbose_name='Nazwa')
    style = tables.Column(verbose_name='Styl')
    ibu = tables.Column(verbose_name='IBU')
    abv = tables.Column(verbose_name='ABV')
    actions = tables.TemplateColumn(accessor='id', verbose_name='Akcje', template_name='pubs/_change_waiting_beers.html')

    class Meta:
        attrs = {'class': 'table', 'data-sortable': 'data-sortable', }
        orderable = False