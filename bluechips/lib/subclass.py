"""
Create subclasses that call out to their "superclass" for all methods
but return the "subclass's" type
"""

def wrapper(cls, func):
    return (lambda self, *args: cls(getattr(self.value, func)(*map(self.value.__class__, args))))

class SmartSubclass(object):
    def __init__(self, superclass, exclude=None):
        if exclude is None:
            exclude = []
        self.superclass = superclass
        self.exclude = exclude
    def __call__(self, name, bases, dict):
        c = type(name, bases, dict)
        for func in dir(self.superclass):
            if func not in dir(c) and \
                callable(getattr(self.superclass, func)) and \
                func not in self.exclude:
                setattr(c, func, wrapper(c, func))
        return c

__all__ = ['SmartSubclass']
