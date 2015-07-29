from app.users.models import Profile


class AddProfile:
    def process_request(self, request):
        request.profile = Profile.get_by_user(request.user)