from braces.views import LoginRequiredMixin, UserPassesTestMixin


class IsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self, user):
        return user.profile.is_admin()


class CanManageTapsMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self, user):
        return user.profile.can_manage_taps()


class CanManageWaitingBeersMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self, user):
        return user.profile.can_manage_waiting_beers()