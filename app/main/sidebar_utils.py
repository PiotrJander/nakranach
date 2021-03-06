# coding=utf-8
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from app.users.models import Profile


class SidebarMenu(object):
    """Represents the sidebar menu.

    :attr fields: a list of SidebarField objects.
    """

    def __init__(self, request):
        """Creates a SidebarMenu object from a request.

        :param request: a HTTPRequest with a user attribute
        """
        super(SidebarMenu, self).__init__()
        self.fields = []
        self.request = request

        # make fields
        self.make_my_profile()
        self.make_users()
        self.make_taps()
        self.make_waiting_beers()
        self.make_beer_database()

    def append_field(self, field):
        """Appends the child field to children attribute."""
        self.determine_if_active(field)
        self.fields.append(field)

    def insert_field(self, i, field):
        """Inserts the child field into children list at the i-th position."""
        self.determine_if_active(field)
        self.fields.insert(i, field)

    def determine_if_active(self, field):
        """Adds active=True attr to the link field whose URL equals the current URL.
        """
        if isinstance(field, SidebarLinkField):
            field.active = field.url == self.request.path
        if isinstance(field, SidebarWrapperField):
            for child in field.children:
                child.active = child.url == self.request.path

    def make_my_profile(self):
        self.append_field(SidebarLinkField(
            name='Mój profil',
            icon='user',
            url_name='accounts_profile_update'
        ))

    def make_users(self):
        u"""
        Makes a field 'Użytkownicy' with a child field 'Lista'.
        'Lista' links to a list of users the logged user can manage.

        The field is only displayed to users who have the role of a pub admin.
        """
        # if the user in not a admin, do nothing
        if not self.request.profile.is_admin():
            return

        # make the fields
        parent = SidebarWrapperField(name='Użytkownicy', icon='users')
        parent.append_field(SidebarChildField(
            name='Lista',
            url_name='user:list',
        ))
        parent.append_field(SidebarChildField(
            name='Zaproś do pubu',
            url_name='user:invite',
        ))
        self.append_field(parent)

    def make_taps(self):
        # check if the user is in a pub
        if self.request.profile.can_manage_taps():
            self.append_field(SidebarLinkField(
                name='Lista kranów',
                icon='home',
                url_name='tap:list',
            ))

    def make_waiting_beers(self):
        if self.request.profile.can_manage_waiting_beers():
            self.append_field(SidebarLinkField(
                name='Magazyn',
                icon='list',
                url_name='pub:waiting_beers',
            ))

    def make_beer_database(self):
        if self.request.profile.can_manage_waiting_beers():
            self.append_field(SidebarLinkField(
                name='Baza piw',
                icon='beer',
                url_name='beers:create',
            ))


class SidebarField(object):
    """Abstract class for fields in the sidebar menu.

    :attr name: displayed field name
    :attr icon: Font Awesome icon class name
    :attr label: optional FieldLabel object
    :attr is_wrapper: true for Wrapper subclass instances,
                      false for Link and Child subclass instances
    """

    def __init__(self, name, icon, label=None):
        super(SidebarField, self).__init__()
        self.name = name
        self.icon = icon
        self.label = label
        self.is_wrapper = False

    def active_str(self):
        """Returns the string 'class="active"' if the field is active. To be used in templates."""
        if hasattr(self, 'active') and self.active:
            return 'class="active"'
        else:
            return ''

    def icon_str(self):
        """Returns a piece of HTML representing the icon."""
        return '<i class="fa fa-%s"></i>' % self.icon

    def label_str(self):
        """Returns a piece of HTML representing the label, or an empty string
        if there is no label."""
        if self.label:
            return unicode(self.label)
        else:
            return ''


class SidebarLinkField(SidebarField):
    """Sidebar field serving as a link.

    :attr url: href attr of the link
    :attr active: boolean field saying whether the field is active at the given view
                    this attr is added by SidebarMenu.determine_if_active
    """

    def __init__(self, name, icon, url_name, kwargs=None, label=None):
        super(SidebarLinkField, self).__init__(name, icon, label)
        self.url = reverse(url_name, kwargs=kwargs)


class SidebarWrapperField(SidebarField):
    """Sidebar field serving as a wrapper for child fields.

    :attr children: a list of child fields
    """
    ANGLE_DOUBLE_DOWN = '<i class="fa fa-angle-double-down i-right"></i>'

    def __init__(self, name, icon, label=None):
        super(SidebarWrapperField, self).__init__(name, icon, label)
        self.children = []
        self.is_wrapper = True

    def append_field(self, child_field):
        """Appends the child field to children attribute."""
        self.children.append(child_field)

    def insert_field(self, i, child_field):
        """Inserts the child field into children list at the i-th position."""
        self.children.insert(i, child_field)

    def visible_str(self):
        """Returns 'class="visible"' if one of its children is active."""
        for child in self.children:
            if child.active:
                return 'class="visible"'
        else:
            return ''

    @property
    def active(self):
        """SidebarWrapperField is defined to be active when one of its children is active."""
        for child in self.children:
            if child.active:
                return True
        else:
            return False


class SidebarChildField(SidebarLinkField):
    """Sidebar field contained within a SidebarWrapperField.

    A list of child fields forms the children attribute of a SidebarWrapperField object.

    Note that icon has no effect for child fields.
    """
    def __init__(self, name, url_name, kwargs=None, label=None):
        super(SidebarChildField, self).__init__(name, 'angle-right', url_name, kwargs=kwargs, label=label)


class SidebarLabel(object):
    """An informative label appended to fields in the sidebar.

    :attr labeltype: label type; if type is 'success', then the label receives a class 'label-success'
    :attr text: label text
    """

    def __init__(self, labeltype, text):
        super(SidebarLabel, self).__init__()
        self.labeltype = labeltype
        self.text = text

    def __unicode__(self):
        return '<span class="label label-%s new-circle">%s</span>' % (self.labeltype, escape(self.text))

