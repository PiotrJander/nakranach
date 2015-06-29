from django.views.generic import ListView


from .models import Profile

class ProfileListView(ListView):
    model = Profile
