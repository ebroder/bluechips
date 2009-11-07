from datetime import date
from bluechips.tests import *

from bluechips import model
from bluechips.model import meta

class TestSpendController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='spend'))
        # Test response...
        response.mustcontain('Add a New Expenditure')
        form = response.form

        user = meta.Session.query(model.User).\
                filter_by(name=u'Charlie Root').one()
        
        form['spender_id'] = user.id
        form['amount'] = '66.78'
        # Make sure date is today.
        today = date.today()
        assert form['date'].value == today.strftime('%m/%d/%Y')
        form['description'] = 'A test expenditure'
        form['shares-0.amount'] = '1'
        form['shares-1.amount'] = '2'
        form['shares-2.amount'] = '3'
        form['shares-3.amount'] = '4'

        response = form.submit()
        response = response.follow()
        response.mustcontain('Expenditure', 'created.')

        e = meta.Session.query(model.Expenditure).\
                order_by(model.Expenditure.id.desc()).first()
        assert e.spender.name == u'Charlie Root'
        assert e.amount == 6678
        assert e.date == today
        assert e.description == u'A test expenditure'

        # Test the split.


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

    def tearDown(self):
        expenditures = meta.Session.query(model.Expenditure).all()
        for e in expenditures:
            meta.Session.delete(e)
        meta.Session.commit()
