from tw import forms
from tw import dynforms
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

class SplitSpendFieldSet(dynforms.GrowingTableFieldSet):
    engine_name = 'genshi'
    children = [
        AccountSelect('account', include_blank=True),
        forms.TextField('share')
        ]

class ComplexSpendForm(dynforms.CustomisedForm, forms.ListForm):
    prevent_multi_submit = False
    class fields(WidgetsList):
        total = AmountField()
        date = forms.CalendarDatePicker(
            validator=validators.DateConverter(not_empty=True))
        description = forms.TextField(
            size=40,
            validator=validators.NotEmpty())
        credits = SplitSpendFieldSet(
            help_text="""
Remember: creditors are people who owe less money to other people as
the result of a transaction.n
""")
        debits = SplitSpendFieldSet(
            help_text="""
Remember: debitors are people who owe more money as the result of a
transaction.
""")

simple_spend_form = SimpleSpendForm()
complex_spend_form = ComplexSpendForm()
