"""
Create subclasses that call out to their "superclass" for all methods
but return the "subclass's" type
"""

from weakref import WeakValueDictionary

def wrapper(c, func):
    return (lambda self,*args: c(getattr(self.value, func)(*map(self.value.__class__, args))))

def __new__(cls, value=0):
    if value not in cls.__old_values__:
        new_object = super(cls, cls).__new__(cls, value)
        cls.__old_values__[value] = new_object
        return new_object
    else:
        return cls.__old_values__[value]

class SmartSubclass(object):
    def __init__(self, superclass, exclude=[]):
        self.superclass = superclass
        self.exclude = exclude
    def __call__(self, name, bases, dict):
        dict['__old_values__'] = WeakValueDictionary()
        dict['__new__'] = __new__
        c = type(name, bases, dict)
        for func in dir(self.superclass):
            if func not in dir(c) and \
                callable(getattr(self.superclass, func)) and \
                func not in self.exclude:
                setattr(c, func, wrapper(c, func))
        return c

__all__ = ['SmartSubclass']
