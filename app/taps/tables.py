from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables


class TapTable(tables.Table):
    tap_number  = tables.Column(verbose_name=_('Kran nr'))
    brewery     = tables.Column(accessor='beer.brewery.name', verbose_name=_('Browar'))
    beer_name   = tables.Column(accessor='beer.name', verbose_name=_('Piwo'))
    actions     = tables.TemplateColumn(accessor='id', verbose_name=_('Akcje'), template_name='taps/_change_beer_form.html')

    # fullname = tables.Column(verbose_name='Nazwisko', default='N/A')
    # email = tables.EmailColumn(accessor='user.email', verbose_name='Adres email')
    # role = tables.Column(accessor='id', verbose_name='Rola')

    class Meta:
        attrs = {'class': 'table', 'data-sortable': 'data-sortable', }
        orderable = False