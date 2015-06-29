# coding=utf-8
from django.core.urlresolvers import reverse
from django.utils.html import escape
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
        self.user = request.user
        # any view which has a sidebar requires that the user is logged in
        # so we can assume that the request has attribute 'user'

        # test fields
        self.make_dashboard()
        self.make_frontend()
        self.make_elements()

        # custom fields
        self.make_users()

    def append_field(self, field):
        """Appends the child field to children attribute."""
        self.fields.append(field)

    def insert_field(self, i, field):
        """Inserts the child field into children list at the i-th position."""
        self.fields.insert(i, field)

    # methods generating three first default lanceng fields
    def make_dashboard(self):
        self.append_field(SidebarLinkField(
            name='Dashboard',
            icon='home',
            url='/dashboard/'
        ))

    def make_frontend(self):
        self.append_field(SidebarLinkField(
            name='Frontend',
            icon='leaf',
            url='/fontend/',
            label=SidebarLabel('danger', 'COMING SOON')
        ))

    def make_elements(self):
        parent = SidebarWrapperField(name='Elements', icon='bug')
        parent.append_field(SidebarChildField(
            name='Primary',
            url='/primary/',
            label=SidebarLabel('success', 'UPDATED')
        ))
        child2 = SidebarChildField(name='Extended', url='/extended/')
        child2.active = True
        parent.append_field(child2)
        self.append_field(parent)

    # methods for real fields

    def make_users(self):
        u"""
        Makes a field 'Użytkownicy' with a child field 'Lista'.
        'Lista' links to a list of users the logged user can manage.

        The field is only displayed to users who have the role of a pub admin.
        """
        try:
            profile = Profile.objects.get(user=self.user.id)
        except Profile.DoesNotExist:
            return
        if not profile.can_manage_users():
            return
        parent = SidebarWrapperField(name='Użytkownicy', icon='bug')
        parent.append_field(SidebarChildField(
            name='Lista',
            # TODO use actual url
            # url=reverse('users:list'),
            url='',
        ))
        self.append_field(parent)


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

    def mark_active(self):
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

    :attr url: URL to which the field points
    :attr active: boolean field saying whether the field is active at the given view
    """

    def __init__(self, name, icon, url, label=None):
        super(SidebarLinkField, self).__init__(name, icon, label)
        self.url = url
        self.active = False


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

    def mark_visible(self):
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
    ANGLE_RIGHT = '<i class="fa fa-angle-right"></i>'

    def __init__(self, name, url, label=None):
        super(SidebarChildField, self).__init__(name, 'bug', url, label)
        # here 'bug' is just a placeholder - icons are not used by child fields


class SidebarLabel(object):
    """An informative label appended to fields in the sidebar.

    :attr label_type: label type; if type is 'success', then the label receives a class 'label-success'
    :attr text: label text
    """

    def __init__(self, label_type, text):
        super(SidebarLabel, self).__init__()
        self.label_type = label_type
        self.text = text

    def __unicode__(self):
        return '<span class="label label-%s new-circle">%s</span>' % (self.label_type, escape(self.text))

