import django_tables2 as tables
from app.users.models import ProfilePub


class ManagedUsersTable(tables.Table):
    fullname = tables.Column(verbose_name='Nazwisko', default='N/A')
    email = tables.EmailColumn(accessor='user.email', verbose_name='Adres email')
    role = tables.Column(accessor='id', verbose_name='Rola')
    actions = tables.TemplateColumn(accessor='id', verbose_name='Akcje', template_name='users/_change_role_form.html')

    class Meta:
        attrs = {'class': 'table', 'data-sortable': 'data-sortable', }
        orderable = False

    def __init__(self, data, *args, **kwargs):
        pub = kwargs.pop('pub')
        self.pub = pub
        super(ManagedUsersTable, self).__init__(data, *args, **kwargs)

    def render_role(self, record):
        return ProfilePub.get_role(profile=record, pub=self.pub)
