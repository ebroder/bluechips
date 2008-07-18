"""
Define special types used in BlueChips
"""

import sqlalchemy as sa
from bluechips.lib.subclass import SmartSubclass

class Currency(object):
    __metaclass__ = SmartSubclass(int)
    def __init__(self, value):
        if isinstance(value, str):
            self.value = int(float(value) * 100)
        else:
            self.value = int(value)
    
    def __int__(self):
        return self.value
    def __float__(self):
        return float(self.value)
    def __long__(self):
        return long(self.value)
    
    def __cmp__(self, other):
        try:
            return self.value.__cmp__(int(other))
        except:
            return self.value.__cmp__(0)
    
    def __mul__(self, other):
        return Currency(self.value * other)
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __str_no_dollar__(self):
        return str(self)[1:]
    
    def __repr__(self):
        return '%s("%s")' % (self.__class__.__name__, str(self))
    def __str__(self):
        sign = '-' if self.value < 0 else ''
        cents = abs(self.value) % 100
        dollars = (abs(self.value) - cents) / 100
        return '$%s%s.%.02d' % (sign, dollars, cents)

class DBCurrency(sa.types.TypeDecorator):
    """
    A type which represents monetary amounts internally as integers.
    
    This avoids binary/decimal float conversion issues
    """
    
    impl = sa.types.Integer
    
    def process_bind_param(self, value, engine):
        return int(value)
    
    def convert_result_value(self, value, engine):
        return Currency(value)
