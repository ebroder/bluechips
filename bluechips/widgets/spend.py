from tw import forms
from tw.api import WidgetsList

from tw.forms import validators

from bluechips.widgets import *

class SimpleSpendForm(forms.ListForm):
    class fields(WidgetsList):
        account = AccountSelect(label_text='Spender')
        amount = AmountField()
        date = forms.CalendarDatePicker(
            validator=validators.DateConverter(not_empty=True))
        description = forms.TextField(
            size=40,
            validator=validators.NotEmpty())

simple_spend_form = SimpleSpendForm()
