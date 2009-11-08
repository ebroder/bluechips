from unittest import TestCase
from bluechips.lib import totals

class TestReorderingSettle(TestCase):
    def test_transfer_minimized(self):
        """
        Test that the number of transfers is actually minimized.

        Taken from a real-world situation, we discovered that failing
        to re-order the debt lists after every transfer could lead to
        extra, unnecessary transfers.
        """
        self.assertEqual(len(totals.settle({'Alice': 100,
                                            'Bob': -85,
                                            'Charlie': 35,
                                            'Dave': -35,
                                            'Eve': -15})),
                         3)

    def test_settle_even(self):
        transfers = totals.settle({'Alice': 0,
                                   'Bob': 0,
                                   'Charlie': 0})
        assert transfers == []
    
    def test_settle_positive(self):
        transfers = totals.settle({'Alice': -50,
                                   'Bob': 100,
                                   'Charlie': -50})
        assert transfers == [('Bob', 'Charlie', 50),
                             ('Bob', 'Alice', 50)]

    def test_settle_uneven_positive(self):
        try:
            transfers = totals.settle({'Alice': -50,
                                       'Bob': -50,
                                       'Charlie': -50})
        except totals.DirtyBooks:
            pass

    def test_settle_uneven_negative(self):
        try:
            transfers = totals.settle({'Alice': 50,
                                       'Bob': 50,
                                       'Charlie': 50})
        except totals.DirtyBooks:
            pass
