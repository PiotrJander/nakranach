from django.contrib.auth.context_processors import auth

from .sidebar_utils import SidebarMenu


def sidebar_menu(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.
    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    # is anonymous needed?
    # if hasattr(request, 'user'):
    #     user = request.user
    # else:
    #     from django.contrib.auth.models import AnonymousUser
    #     user = AnonymousUser()

    # user = request.user
    # perms = PermWrapper(user)

    return {
        'sidebar_menu': SidebarMenu(request),
    }