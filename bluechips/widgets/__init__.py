from tw import forms

from bluechips import model
from bluechips.model import meta

class UserSelect(forms.SingleSelectField):
    @staticmethod
    def getUserList():
        for u in meta.Session.query(model.User):
            yield (u.username, u.name)
    
    options = getUserList

__all__ = ['UserSelect']
