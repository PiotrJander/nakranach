# coding=utf-8
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit, Div, Hidden
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


class AccountsFormField(Field):
    """
    Extends the Field class and introduces two modifications:
    1) uses custom template
    2) has 'icon' attr
    """
    template = 'crispy/accounts_form_field.html'

    def __init__(self, *args, **kwargs):
        """Sets 'icon' attr on the objects. Use 'icon' kwarg or default 'sign-in' string."""
        icon = kwargs.pop('icon', 'sign-in')  # use 'sign-in' icon by default
        self.icon = icon
        super(AccountsFormField, self).__init__(*args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        """Sets 'field_icon' context variable to self.icon."""
        context['field_icon'] = self.icon
        return super(AccountsFormField, self).render(form, form_style, context, template_pack)


# form helpers

class LoginFormHelper(FormHelper):
    def __init__(self, form=None):
        super(LoginFormHelper, self).__init__(form)
        self.form_action = 'auth_login'
        self.html5_required = True
        self.layout = Layout(
            AccountsFormField('username', wrapper_class='login-input', placeholder='Email', icon='envelope'),
            AccountsFormField('password', css_class='text-input', wrapper_class='login-input', placeholder=u'Hasło',
                              icon='key'),
            'remember_me',
            HTML(u'''
            <div class="row">
              <div class="col-sm-6">
                <button type="submit" class="btn btn-success btn-block"><i class="fa fa-unlock"></i> Zaloguj się</button>
              </div>
              <div class="col-sm-6"><a href="{% url 'registration_register' %}" class="btn btn-default btn-block"><i class="fa fa-rocket"></i> Załóż konto</a></div>
            </div>
        ''')
        )


class RegisterFormHelper(FormHelper):
    def __init__(self, form=None):
        super(RegisterFormHelper, self).__init__(form)
        self.form_action = 'registration_register'
        self.html5_required = True
        self.layout = Layout(
            AccountsFormField('email', css_class='text-input', wrapper_class='login-input', placeholder='Email',
                              icon='envelope'),
            AccountsFormField('name', wrapper_class='login-input', placeholder=u'Imię', icon='user'),
            AccountsFormField('surname', wrapper_class='login-input', placeholder='Nazwisko', icon='user'),
            AccountsFormField('password1', css_class='text-input', wrapper_class='login-input', placeholder=u'Hasło',
                              icon='key'),
            AccountsFormField('password2', css_class='text-input', wrapper_class='login-input',
                              placeholder=u'Powtórz hasło', icon='eye'),
            Submit('submit', u'Załóż konto', css_class='btn btn-success btn-block')
        )


class PasswordResetConfirmFormHelper(FormHelper):
    def __init__(self, form=None):
        super(PasswordResetConfirmFormHelper, self).__init__(form)
        self.html5_required = True
        self.layout = Layout(
            AccountsFormField('new_password1', css_class='text-input', wrapper_class='login-input',
                              placeholder=u'Nowe hasło', icon='key'),
            AccountsFormField('new_password2', css_class='text-input', wrapper_class='login-input',
                              placeholder=u'Powtórz hasło', icon='eye'),
            Submit('submit', u'Zresetuj hasło', css_class='btn btn-success btn-block')
        )


class PasswordChangeFormHelper(FormHelper):
    def __init__(self, form=None):
        super(PasswordChangeFormHelper, self).__init__(form)
        self.html5_required = True
        self.layout = Layout(
            Div('old_password', 'new_password1', 'new_password2', css_class='modal-body'),
            Div(
                StrictButton('Anuluj', css_class='btn btn-default', data_dismiss='modal'),
                StrictButton(u'Zresetuj hasło', type='submit', name='action',
                             value='password_change', css_class='btn btn-success'),

                css_class='modal-footer',
            )
        )


class ProfileUpdateFormHelper(FormHelper):
    def __init__(self, form=None):
        super(ProfileUpdateFormHelper, self).__init__(form)
        self.layout = Layout(
            'email', 'old_email', 'name', 'surname',
            StrictButton(u'Zmień dane', type='submit', name='action', value='email_name', css_class='btn btn-default'),
        )