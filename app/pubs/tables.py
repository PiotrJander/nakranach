import django_tables2 as tables


class WaitingBeersTable(tables.Table):
    brewery = tables.Column()
    name = tables.Column()
    style = tables.Column()
    ibu = tables.Column()
    abv = tables.Column()
    actions = tables.TemplateColumn(accessor='id', verbose_name='Akcje', template_name='pubs/_change_waiting_beers.html')

    class Meta:
        attrs = {'class': 'table', 'data-sortable': 'data-sortable', }
        orderable = False