"""
Define special types used in BlueChips
"""

import sqlalchemy as sa
from sqlalchemy.types import *
from bluechips.lib.subclass import SmartSubclass

from enum import Enum

from weakref import WeakValueDictionary

class Currency(object):
    """
    Store currency values as an integral number of cents
    """
    __metaclass__ = SmartSubclass(int)
    __old_values__ = WeakValueDictionary()
    def __new__(cls, value):
        if isinstance(value, str):
            value = int(float(value) * 100)
        else:
            value = int(value)
        
        if value not in cls.__old_values__:
            new_object = super(cls, cls).__new__(cls)
            new_object.value = value
            cls.__old_values__[value] = new_object
            return new_object
        else:
            return cls.__old_values__[value]
    
    def __int__(self):
        """
        If I don't define this, SmartSubclass will return
        Currency(int(self.value))
        """
        return self.value
    def __float__(self):
        """
        If I don't define this, SmartSubclass will return
        Currency(float(self.value))
        """
        return float(self.value)
    def __long__(self):
        """
        If I don't define this, SmartSubclass will return
        Currency(long(self.value))
        """
        return long(self.value)
    
    def __cmp__(self, other):
        """
        This is overridden for when validators compare a Currency to
        ''
        """
        if other == '':
            return 1
        else:
            return self.value.__cmp__(int(other))
    
    def __mul__(self, other):
        """
        If I don't define this, SmartSubclass will convert the other
        argument to an int
        """
        return Currency(self.value * other)
    def __rmul__(self, other):
        """
        If I don't define this, SmartSubclass will convert the other
        argument to an int
        """
        return self.__mul__(other)
    
    def __str_no_dollar__(self):
        """
        Get to the formatted string without the dollar sign
        """
        return str(self).replace('$', '')
    
    def __repr__(self):
        return '%s("%s")' % (self.__class__.__name__, str(self))
    def __str__(self):
        sign = '-' if self.value < 0 else ''
        cents = abs(self.value) % 100
        dollars = (abs(self.value) - cents) / 100
        return '%s$%s.%.02d' % (sign, dollars, cents)

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

__all__ = ['Currency', 'DBCurrency', 'Enum']
__all__.append(sa.types.__all__)
