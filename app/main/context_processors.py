from django.contrib.auth.context_processors import auth

from .sidebar_utils import SidebarMenu


def sidebar_menu(request):
    """
    Adds 'sidebar_menu' to the context. Only takes effect when the user is logged in.
    """
    if request.path.startswith('/admin/'):
        return {}
        # not applicable at admin sites
    if request.user.is_authenticated():
        return { 'sidebar_menu': SidebarMenu(request), }
    else:
        return {}