from tw import forms

from tw.forms import validators

from bluechips import model
from bluechips.model import meta

from decimal import Decimal

class UserSelect(forms.SingleSelectField):
    @staticmethod
    def getUserList():
        for u in meta.Session.query(model.User):
            yield (u.id, u.name)
    
    options = getUserList
    validator = validators.Wrapper(
        to_python=(lambda x: meta.Session.query(model.User).get(int(x))),
        from_python=(lambda x: str(x.id)))
    
    def _is_option_selected(self, option_value, value):
        return option_value == value.id

class AmountField(forms.TextField):
    size = 8
    validator = validators.All(
        validators.Wrapper(
            to_python=Decimal,
            from_python=str),
        validators.Regex(r'^[0-9]*(\.[0-9]{2})?$', not_empty=True))

__all__ = ['UserSelect', 'AmountField']
