from tw import forms
from tw.api import WidgetsList

from tw.forms import validators

from bluechips.widgets import *
from bluechips import model
from bluechips.model.meta import Session

class _SplitFieldset(forms.ListFieldSet):
    def getChildren():
        try:
            resident_share = 100.0 / float(Session.query(model.User).count())
        except ZeroDivisionError:
            resident_share = 0
        for u in Session.query(model.User):
            yield forms.TextField('%s' % u.id,
                                  label_text=u.name,
                                  default=(resident_share if u.resident else 0))
    
    children = getChildren()

class NewSpendForm(forms.ListForm):
    class fields(WidgetsList):
        spender = UserSelect()
        amount = AmountField()
        date = forms.CalendarDatePicker(
            validator=validators.DateConverter(not_empty=True))
        description = forms.TextField(size=40)
        split = _SplitFieldset(suppress_label=True)

new_spend_form = NewSpendForm()
