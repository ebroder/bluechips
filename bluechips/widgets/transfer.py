from tw import forms
from tw.api import WidgetsList

from tw.forms import validators

from bluechips.widgets import *

class NewTransferForm(forms.ListForm):
    class fields(WidgetsList):
        debtor = AccountSelect()
        creditor = AccountSelect()
        amount = AmountField()
        date = forms.CalendarDatePicker(
            validator=validators.DateConverter(not_empty=True))
        description = forms.TextField(size=40)
    
    validator = validators.Schema(
        chained_validators=[
            FieldsDontMatch('debtor', 'creditor',
                            messages=dict(
                    invalid="Can't transfer to yourself!"))])

new_transfer_form = NewTransferForm()
