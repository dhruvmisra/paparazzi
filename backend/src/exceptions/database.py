# -*- coding: utf-8 -*-
from .base import ApplicationException


class DatabaseException(ApplicationException):
    """Generic Database Exception"""


class RecordNotFoundException(DatabaseException):
    """Record not found in database"""
