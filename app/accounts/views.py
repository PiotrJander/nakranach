from registration.backends.simple.views import RegistrationView
from app.accounts.forms import CustomUserRegistrationForm
from app.users.models import Profile


class ProfileRegistrationView(RegistrationView):
    """
    Works like RegistrationFormUniqueEmail, but on saving the user also creates a Profile and links that profile
    to the newly created user. Also handles first name and last name fields.
    """
    form_class = CustomUserRegistrationForm
    success_url = 'main:dashboard'

    def register(self, request, form):
        new_user = super(ProfileRegistrationView, self).register(request, form)
        Profile.objects.create(user=new_user, name=form.cleaned_data['first_name'],
                               surname=form.cleaned_data['last_name'])
        return new_user
