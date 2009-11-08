from datetime import date
from formencode import Invalid

from bluechips.tests import *

from bluechips import model
from bluechips.model import meta
from bluechips.model.types import Currency

from bluechips.controllers.spend import ExpenditureSchema

class TestSpendController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='spend'))
        # Test response...
        response.mustcontain('Add a New Expenditure')
        form = response.form

        user = meta.Session.query(model.User).\
                filter_by(name=u'Charlie Root').one()
        
        form['spender_id'] = user.id
        form['amount'] = '74.04'
        # Make sure date is today.
        today = date.today()
        assert form['date'].value == today.strftime('%m/%d/%Y')
        form['description'] = 'A test expenditure'
        form['shares-0.amount'] = '1'
        form['shares-1.amount'] = '2'
        form['shares-2.amount'] = '2'
        form['shares-3.amount'] = '1'
        for ii in range(4):
            assert int(form['shares-%d.user_id' % ii].value) == ii + 1

        response = form.submit()
        response = response.follow()
        response.mustcontain('Expenditure', 'created.')

        e = meta.Session.query(model.Expenditure).\
                order_by(model.Expenditure.id.desc()).first()
        assert e.spender.name == u'Charlie Root'
        assert e.amount == 7404
        assert e.date == today
        assert e.description == u'A test expenditure'

        # Test the split.
        shares = dict(((sp.user_id, sp.share)
                       for sp in e.splits))
        assert shares[1] == Currency('12.34')
        assert shares[2] == Currency('24.68')
        assert shares[3] == Currency('24.68')
        assert shares[4] == Currency('12.34')


    def test_edit(self):
        user = meta.Session.query(model.User).\
                filter_by(name=u'Charlie Root').one()
        e = model.Expenditure(user, 53812, u'Lemon bundt cake', None)
        e.even_split()
        meta.Session.add(e)
        meta.Session.commit()

        response = self.app.get(url_for(controller='spend',
                                        action='edit',
                                        id=e.id))
        response.mustcontain('Edit an Expenditure')
        form = response.form

        assert int(form['spender_id'].value) == user.id
        assert form['amount'].value == '538.12'
        assert form['date'].value == date.today().strftime('%m/%d/%Y')
        assert form['description'].value == u'Lemon bundt cake'

        form['description'] = u'Updated bundt cake'

        # Update the split too.

        response = form.submit()
        response = response.follow()
        response.mustcontain('Expenditure', 'updated.')

        e = meta.Session.query(model.Expenditure).\
                order_by(model.Expenditure.id.desc()).first()
        assert e.description == u'Updated bundt cake'

    def test_edit_nonexistent(self):
        response = self.app.get(url_for(controller='spend',
                                        action='edit',
                                        id=124234), status=404)

    def test_update_nonexistent(self):
        response = self.app.post(url_for(controller='spend',
                                         action='update',
                                         id=14234), 
                                 params=self.sample_post,
                                 status=404)

    def test_all_zero_shares_fails(self):
        params = self.sample_post.copy()
        for ii in range(4):
            params['shares-%d.amount' % ii] = '0'
        v = ExpenditureSchema()
        try:
            v.to_python(params)
        except Invalid:
            pass

    def setUp(self):
        self.sample_post = {
            'spender_id': '1',
            'amount': '44.12',
            'date': '10/5/2008',
            'description': 'Example expenditure post data.',
            'shares-0.user_id': '1',
            'shares-0.amount': '1',
            'shares-1.user_id': '2',
            'shares-1.amount': '1',
            'shares-2.user_id': '3',
            'shares-2.amount': '1',
            'shares-3.user_id': '4',
            'shares-3.amount': '1'}

    def tearDown(self):
        expenditures = meta.Session.query(model.Expenditure).all()
        for e in expenditures:
            meta.Session.delete(e)
        meta.Session.commit()
