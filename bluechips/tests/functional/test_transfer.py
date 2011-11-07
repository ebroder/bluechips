from datetime import date
from decimal import Decimal

from webhelpers.pylonslib.secure_form import token_key

from bluechips.tests import *
from bluechips import model
from bluechips.model import meta

class TestTransferController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='transfer',
                                        action='index'))
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
        response.mustcontain('Transfer', 'created.')

        t = meta.Session.query(model.Transfer).\
                order_by(model.Transfer.id.desc()).first()
        assert t.debtor.name == u'Rich Scheme'
        assert t.creditor.name == u'Ben Bitdiddle'
        assert t.amount == 12345
        assert t.date == today
        assert t.description == u'A test transfer from Rich to Ben'

    def test_edit_and_delete(self):
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
        response.mustcontain('Transfer', 'updated.')

        t = meta.Session.query(model.Transfer).\
                order_by(model.Transfer.id.desc()).first()
        assert t.description == u'A new description'

        response = self.app.get(url_for(controller='transfer',
                                        action='delete',
                                        id=t.id))
        response = response.form.submit('delete').follow()
        response.mustcontain('Transfer', 'deleted')

    def test_edit_nonexistent(self):
        response = self.app.get(url_for(controller='transfer',
                                        action='edit',
                                        id=21424), status=404)

    def test_update_nonexistent(self):
        response = self.app.get(url_for(controller='transfer',
                                        action='edit'))
        params = self.sample_params.copy()
        params[token_key] = response.form[token_key].value
        self.app.post(url_for(controller='transfer',
                              action='update',
                              id=21424),
                      params=params,
                      status=404)

    def test_xsrf_protection(self):
        self.app.post(url_for(controller='transfer',
                              action='update'),
                      params=self.sample_params,
                      status=403)


    def test_update_get_redirects(self):
        response = self.app.get(url_for(controller='transfer',
                                        action='update'),
                                status=302)
        assert (dict(response.headers)['Location'] ==
                url_for(controller='transfer', action='edit', qualified=True))

    def test_delete_nonexistent(self):
        self.app.get(url_for(controller='transfer',
                             action='delete',
                             id=124244),
                     status=404)

    def test_destroy_nonexistent(self):
        response = self.app.get(url_for(controller='transfer',
                                        action='edit'))
        params = self.sample_params.copy()
        params[token_key] = response.form[token_key].value
        self.app.post(url_for(controller='transfer',
                              action='destroy',
                              id=124344), 
                      params=params,
                      status=404)

    def test_delete_xsrf_protection(self):
        self.app.post(url_for(controller='transfer',
                              action='destroy',
                              id=1),
                      params={'delete': 'Delete'},
                      status=403)

    def setUp(self):
        self.sample_params = {
            'debtor_id': '1',
            'creditor_id': '2',
            'amount': '33.98',
            'date': '4/1/2007',
            'description': 'Example transfer params.'}

    def tearDown(self):
        transfers = meta.Session.query(model.Transfer).all()
        for t in transfers:
            meta.Session.delete(t)
        meta.Session.commit()
