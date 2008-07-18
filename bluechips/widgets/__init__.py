from tw import forms

from tw.forms import validators

from bluechips import model
from bluechips.model import meta

from bluechips.model.types import Currency

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
        if value is not None:
            return option_value == value.id
        else:
            return False

class AmountField(forms.TextField):
    size = 8
    validator = validators.All(
        validators.Wrapper(
            to_python=(lambda x: Currency(float(x) * 100)),
            from_python=Currency.__str_no_dollar__),
        validators.Regex(r'^[0-9]*(\.[0-9]{2})?$'))

# This is virtually copied from formencode.validator.FieldsMatch, but
# I wanted my own version for fields that shouldn't match
class FieldsDontMatch(validators.FormValidator):
    """
    Tests that the given fields do not match.
    """
    
    show_match = False
    field_names = None
    valid_partial_form = True
    __unpackargs__ = ('*', 'field_names')
    
    messages = {
        'invalid': "Fields match"
        }
    
    def validate_partial(self, field_dict, state):
        for name in self.field_names:
            if not field_dict.has_key(name):
                return
        self.validate_python(field_dict, state)
    
    def validate_python(self, field_dict, state):
        errors = {}
        for ref_index, ref in enumerate(self.field_names):
            for name in self.field_names[ref_index+1:]:
                if field_dict.get(name, '') == field_dict.get(ref, ''):
                    errors[name] = self.message('invalid', state)
        if errors:
            error_list = errors.items()
            error_list.sort()
            error_message = '<br>\n'.join(
                ['%s: %s' % (name, value) for name, value in error_list])
            raise validators.Invalid(error_message,
                                     field_dict, state,
                                     error_dict=errors)

__all__ = ['UserSelect', 'AmountField', 'FieldsDontMatch']
