from tw import forms
from tw.api import WidgetsList

from tw.forms import validators

from bluechips.widgets import *

forms.FormField.engine_name = 'mako'

class NewSpendForm(forms.ListForm):
    class fields(WidgetsList):
        spender = UserSelect()

new_spend_form = NewSpendForm()
