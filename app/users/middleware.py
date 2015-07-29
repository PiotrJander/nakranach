from app.users.models import Profile


class AddProfile(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            request.profile = Profile.get_by_user(request.user)