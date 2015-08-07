# coding=utf-8
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML


class ChangeBeerOnTapFormHelper(FormHelper):
    def __init__(self, form=None):
        super(ChangeBeerOnTapFormHelper, self).__init__(form)
        self.layout = Layout(
            Div(
                HTML(u'''<p>Wybierz nowe piwo, którym zastąpisz piwo <span id="beerName"></span>
                na kranie <span id="tapNo"></span></p>'''),
                'new_beer',
                css_class='modal-body'
            ),
            Div(
                StrictButton('Pozostaw piwo', type='button', data_dismiss='modal', css_class='btn btn-default'),
                css_class='modal-footer'
            ),
        )
