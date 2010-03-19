"""
Define special types used in BlueChips
"""

import locale
from decimal import Decimal, InvalidOperation

import sqlalchemy as sa
from formencode import validators, Invalid
from bluechips.lib.subclass import SmartSubclass

from weakref import WeakValueDictionary

def localeconv():
    "Manually install en_US for systems that don't have it."
    d = {'currency_symbol': '$',
     'decimal_point': '.',
     'frac_digits': 2,
     'grouping': [3, 3, 0],
     'int_curr_symbol': 'USD ',
     'int_frac_digits': 2,
     'mon_decimal_point': '.',
     'mon_grouping': [3, 3, 0],
     'mon_thousands_sep': ',',
     'n_cs_precedes': 1,
     'n_sep_by_space': 0,
     'n_sign_posn': 1,
     'negative_sign': '-',
     'p_cs_precedes': 1,
     'p_sep_by_space': 0,
     'p_sign_posn': 1,
     'positive_sign': '',
     'thousands_sep': ','}
    return d
locale.localeconv = localeconv


class CurrencyValidator(validators.FancyValidator):
    "A validator to convert to Currency objects."
    messages = {'amount': "Please enter a valid currency amount",
                'precision': "Only two digits after the decimal, please",
                'nonzero': "Please enter a non-zero amount"}

    def _to_python(self, value, state):
        try:
            dec = Decimal(value)
        except InvalidOperation:
            raise Invalid(self.message('amount', state),
                          value, state)
        else:
            ret = dec.quantize(Decimal('1.00'))
            if ret == 0:
                raise Invalid(self.message('nonzero', state),
                              value, state)
            elif ret != dec:
                raise Invalid(self.message('precision', state),
                              value, state)
            else:
                return Currency(int(ret * 100))


class Currency(object):
    """
    Store currency values as an integral number of cents
    """
    __metaclass__ = SmartSubclass(int)
    __old_values__ = WeakValueDictionary()
    def __new__(cls, value):
        if value is None:
            value = 0
        elif isinstance(value, str):
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
    def __div__(self, other):
        """
        If I don't define this, SmartSubclass will convert the other
        argument to an int
        """
        return Currency(self.value / other)
    def __truediv__(self, other):
        """
        If I don't define this, SmartSubclass will convert the other
        argument to an int
        """
        return Currency(self.value / other)
    
    def __repr__(self):
        return '%s("%s")' % (self.__class__.__name__, str(self))
    def __str__(self):
        return locale.currency(self.value / 100., grouping=True)


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
    process_result_value = convert_result_value
