from django.contrib.auth.context_processors import auth
from app.users.models import Profile

from .sidebar_utils import SidebarMenu


def sidebar_menu(request):
    """
    Adds 'sidebar_menu' to the context. Only takes effect when the user is logged in.
    """
    if hasattr(request.user, 'profile'):
        return { 'sidebar_menu': SidebarMenu(request) }
    else:
        return {}


def profile(request):
    """Adds 'profile' to the context. Only takes effect when the user is logged in."""
    if hasattr(request.user, 'profile'):
        return {'profile': request.user.profile }
    else:
        return {}