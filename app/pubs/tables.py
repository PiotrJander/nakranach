import django_tables2 as tables


class WaitingBeersTable(tables.Table):
    brewery = tables.Column()
    name = tables.Column()
    style = tables.Column()
    ibu = tables.Column()
    abv = tables.Column()
    actions = tables.TemplateColumn()