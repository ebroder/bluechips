from datetime import date
from decimal import Decimal
from bluechips.tests import *

from bluechips import model
from bluechips.model import meta

class TestTransferController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='transfer'))
        # Test response...
        response.mustcontain('Add a New Transfer')
        form = response.form

        user_rich = meta.Session.query(model.User).\
                filter_by(name=u'Rich Scheme').one()
        user_ben = meta.Session.query(model.User).\
                filter_by(name=u'Ben Bitdiddle').one()

        form['debtor_id'] = user_rich.id
        form['creditor_id'] = user_ben.id
        form['amount'] = '123.45'
        # Make sure date is today.
        today = date.today()
        assert form['date'].value == today.strftime('%m/%d/%Y')
        form['description'] = 'A test transfer from Rich to Ben'

        response = form.submit()
        response = response.follow()
        response.mustcontain('Transfer updated.')

        t = meta.Session.query(model.Transfer).\
                order_by(model.Transfer.id.desc()).first()
        assert t.debtor.name == u'Rich Scheme'
        assert t.creditor.name == u'Ben Bitdiddle'
        assert t.amount == 12345
        assert t.date == today
        assert t.description == u'A test transfer from Rich to Ben'
        meta.Session.delete(t)
        meta.Session.commit()

    def test_edit(self):
        user_rich = meta.Session.query(model.User).\
                filter_by(name=u'Rich Scheme').one()
        user_ben = meta.Session.query(model.User).\
                filter_by(name=u'Ben Bitdiddle').one()
        t = model.Transfer(user_rich, user_ben, 12345)
        t.description = u'Test transfer'
        meta.Session.add(t)
        meta.Session.commit()

        response = self.app.get(url_for(controller='transfer',
                                        action='edit',
                                        id=t.id))
        response.mustcontain('Edit a Transfer')
        form = response.form

        assert int(form['debtor_id'].value) == t.debtor_id
        assert int(form['creditor_id'].value) == t.creditor_id
        assert Decimal(form['amount'].value) * 100 == t.amount
        assert form['date'].value == t.date.strftime('%m/%d/%Y')
        assert form['description'].value == t.description

        form['description'] = u'A new description'

        response = form.submit()
        response = response.follow()
        response.mustcontain('Transfer updated.')

        t = meta.Session.query(model.Transfer).\
                order_by(model.Transfer.id.desc()).first()
        assert t.description == u'A new description'
        meta.Session.delete(t)
        meta.Session.commit()
