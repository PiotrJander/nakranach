# coding=utf-8
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
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
        AccountsFormField('username', wrapper_class='login-input', placeholder='Email', icon='sign-in'),
        AccountsFormField('password', css_class='text-input', wrapper_class='login-input', placeholder=u'Hasło', icon='key'),
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
