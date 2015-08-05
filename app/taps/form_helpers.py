# coding=utf-8
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML


class ChangeBeerOnTapFormHelper(FormHelper):
    def __init__(self, form=None):
        super(ChangeBeerOnTapFormHelper, self).__init__(form)
        self.layout = Layout(
            'tap_id',
            Div(
                HTML(u'''<p>Wybierz nowe piwo, którym zastąpisz piwo <span id="beerName"></span>
                na kranie <span id="tapNo"></span></p>'''),
                'waiting_beers',
                css_class='modal-body'
            ),
            Div(
                StrictButton('Pozostaw piwo', type='button', data_dismiss='modal', css_class='btn btn-default'),
                StrictButton(u'Zmień piwo', type='submit', name='action', value='change',
                             css_class='btn btn-primary'),
                css_class='modal-footer'
            ),
        )