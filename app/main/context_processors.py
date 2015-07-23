from django.contrib.auth.context_processors import auth
from app.users.models import Profile

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


def profile(request):
    """Adds 'profile' to the context. Only takes effect when the user is logged in."""
    if request.path.startswith('/admin/'):
        return {}
        # not applicable at admin sites
    if request.user.is_authenticated():
        return {'profile': Profile.get_by_user(request.user)}
    else:
        return {}