# coding=utf-8
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit, Div, Hidden
from django.conf import settings


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
        super(AccountsFormField, self).__init__(*args, **kwargs)
        self.icon = icon

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        """Sets 'field_icon' context variable to self.icon."""
        context['field_icon'] = self.icon
        return super(AccountsFormField, self).render(form, form_style, context, template_pack)


# login form helper

login_form_helper = FormHelper()
login_form_helper.__dict__.update({
    'form_action': 'auth_login',
    'html5_required': True,
    'layout': Layout(
        AccountsFormField('username', wrapper_class='login-input', placeholder='Email', icon='envelope'),
        AccountsFormField('password', css_class='text-input', wrapper_class='login-input', placeholder=u'Hasło', icon='key'),
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
})


# register form helper

register_form_helper = FormHelper()
register_form_helper.__dict__.update({
    'form_action': 'registration_register',
    'html5_required': True,
    'layout': Layout(
        AccountsFormField('email', css_class='text-input', wrapper_class='login-input', placeholder='Email', icon='envelope'),
        AccountsFormField('first_name', wrapper_class='login-input', placeholder=u'Imię', icon='user'),
        AccountsFormField('last_name', wrapper_class='login-input', placeholder='Nazwisko', icon='user'),
        AccountsFormField('password1', css_class='text-input', wrapper_class='login-input', placeholder=u'Hasło', icon='key'),
        AccountsFormField('password2', css_class='text-input', wrapper_class='login-input', placeholder=u'Powtórz hasło', icon='eye'),
        Submit('submit', u'Załóż konto', css_class='btn btn-success btn-block')
    )
})


# password reset confirm form helper

password_reset_confirm_form_helper = FormHelper()
password_reset_confirm_form_helper.__dict__.update({
    'form_action': 'auth_password_reset_confirm',
    'html5_required': True,
    'layout': Layout(
        AccountsFormField('new_password1', css_class='text-input', wrapper_class='login-input', placeholder=u'Nowe hasło', icon='key'),
        AccountsFormField('new_password2', css_class='text-input', wrapper_class='login-input', placeholder=u'Powtórz hasło', icon='eye'),
        Submit('submit', u'Zresetuj hasło', css_class='btn btn-success btn-block')
    )
})


# password change form helper

password_change_form_helper = FormHelper()
password_change_form_helper.__dict__.update({
    # 'form_action': '/accounts/password/change/',
    # 'form_action': 'accounts_profile_update',
    'attrs': {'action': '/accounts/profile/update/'},
    'html5_required': True,
    'layout': Layout(
        Hidden('password_change', 'password_change'),
        Div('old_password', 'new_password1', 'new_password2', css_class='modal-body'),
        Div(
            HTML(u'<button type="button" class="btn btn-default" data-dismiss="modal">Anuluj</button>'),
            Submit('submit', u'Zresetuj hasło', css_class='btn btn-success'),
            css_class='modal-footer',
        )
    )
})


# profile update form helper

profile_update_form_helper = FormHelper()
# profile_update_form_helper.form_action('')
profile_update_form_helper.add_input(Submit('submit', u'Zmień dane', css_class='btn btn-default'))