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

        transfer = meta.Session.query(model.Transfer).\
                order_by(model.Transfer.id.desc()).first()
        assert transfer.debtor.name == u'Rich Scheme'
        assert transfer.creditor.name == u'Ben Bitdiddle'
        assert transfer.amount == 12345
        assert transfer.date == today
        assert transfer.description == u'A test transfer from Rich to Ben'

    def test_edit(self):
        user_rich = meta.Session.query(model.User).\
                filter_by(name=u'Rich Scheme').one()
        user_ben = meta.Session.query(model.User).\
                filter_by(name=u'Ben Bitdiddle').one()
        transfer = model.Transfer(user_rich, user_ben, 12345)
        transfer.description = u'Test transfer'
        meta.Session.add(transfer)
        meta.Session.commit()

        response = self.app.get(url_for(controller='transfer',
                                        action='edit',
                                        id=transfer.id))
        response.mustcontain('Edit a Transfer')
        form = response.form

        assert int(form['debtor_id'].value) == transfer.debtor_id
        assert int(form['creditor_id'].value) == transfer.creditor_id
        assert Decimal(form['amount'].value) * 100 == transfer.amount
        assert form['date'].value == transfer.date.strftime('%m/%d/%Y')
        assert form['description'].value == transfer.description

        form['description'] = u'A new description'

        response = form.submit()
        response = response.follow()
        response.mustcontain('Transfer updated.')

        transfer = meta.Session.query(model.Transfer).\
                order_by(model.Transfer.id.desc()).first()
        assert transfer.description == u'A new description'
