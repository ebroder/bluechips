from tw import forms

from tw.forms import validators

from bluechips import model
from bluechips.model import meta

class UserSelect(forms.SingleSelectField):
    @staticmethod
    def getUserList():
        for u in meta.Session.query(model.User):
            yield (u.id, u.name)
    
    options = getUserList
    validator = validators.Wrapper(
        to_python=meta.Session.query(model.User).get,
        from_python=(lambda x: x.id))

class AmountField(forms.TextField):
    size = 8
    validator = validators.All(
        validators.Number(),
        validators.Regex(r'^[0-9]*(\.[0-9]{2})?$', not_empty=True))

__all__ = ['UserSelect', 'AmountField']
