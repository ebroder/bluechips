import sqlalchemy as sa
from bluechips.model import types
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

# Base from which the declarative classes are derived
Base = declarative_base()

def BlueChipsTable(cls):
    cls.created_at = sa.Column(types.DateTime, default=datetime.utcnow)
    cls.updated_at = sa.Column(types.DateTime, onupdate=datetime.utcnow)
    
    return cls

__all__ = ['Base', 'BlueChipsTable']
