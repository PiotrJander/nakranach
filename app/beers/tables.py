import django_tables2 as tables


class BeersTable(tables.Table):
    brewery = tables.Column(verbose_name='Browar')
    name = tables.Column(verbose_name='Nazwa')
    style = tables.Column(verbose_name='Styl')

    class Meta:
        attrs = {'class': 'table', 'data-sortable': 'data-sortable', }
        orderable = False