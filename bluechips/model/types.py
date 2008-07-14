"""
Define special types used in BlueChips
"""

import sqlalchemy as sa
from bluechips.lib.helpers import round_currency
import locale

class Currency(sa.types.TypeDecorator):
    """
    A type which represents monetary amounts internally as integers.
    
    This avoids binary/decimal float conversion issues
    """
    
    impl = sa.types.Integer
    
    def process_bind_param(self, value, engine):
        return int(value * 100)
    
    def convert_result_value(self, value, engine):
        return round_currency(Decimal(value) / 100)
