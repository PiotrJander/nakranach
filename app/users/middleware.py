from app.users.models import Profile


class AddProfile(object):

    def process_request(self, request):
        if request.user.is_authenticated() and hasattr(request.user, 'profile'):
            request.profile = request.user.profile
