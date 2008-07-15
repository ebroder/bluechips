from tw import forms
from tw.api import WidgetsList

from tw.forms import validators

from bluechips.widgets import *

class NewSpendForm(forms.ListForm):
    class fields(WidgetsList):
        spender = UserSelect()
        amount = AmountField()
        date = forms.CalendarDatePicker(
            validator=validators.DateConverter(not_empty=True))
        description = forms.TextField(
            size=40,
            validator=validators.NotEmpty())

new_spend_form = NewSpendForm()
