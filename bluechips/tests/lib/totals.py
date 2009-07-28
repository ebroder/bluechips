from unittest import TestCase
from bluechips.lib import totals

class TestReorderingSettle(TestCase):
    def test(self):
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
