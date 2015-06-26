from .sidebar_utils import SidebarMenu

class SidebarMenuMiddleware:
    def process_template_response(self, request, response):
        """
        Adds a 'sidebar_menu' entry to the context dictionary.

        Assumes there are already 'user' and 'perms' entries in the context,
        added by django.contrib.auth.context_processors.auth
        """
        user = response.context_data['user']
        perms = response.context_data['perms']
        response.context_data['sidebar_menu'] = SidebarMenu()
        return response