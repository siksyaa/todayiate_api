# -*- coding: utf-8 -*-
"""
Constant 정의
"""
from __future__ import unicode_literals

from .core import main


class EnumConstantMeta(type):
    @staticmethod
    def __new__(cls, name, bases, dct):
        dct['reverse_mapping'] = {
            value: key
            for key, value in dct.iteritems() if not key.startswith('__')
            }

        return super(EnumConstantMeta, cls).__new__(cls, name, bases, dct)

    def __setattr__(cls, key, value):
        raise TypeError('cannot set a value to Enum.')

    def __repr__(cls):
        return '<EnumConstant.%s>' % cls.__name__


class EnumConstant(object):
    __metaclass__ = EnumConstantMeta


@main.context_processor
def inject_constants():
    return dict()


class SCHEDULE_STATUS(EnumConstant):
    SCHEDULED = 0
    QUEUED = 1
    COMPLETED = 2
    CANCELED = -1
    FAILED = -2


class SCHEDULE_TYPE(EnumConstant):
    ONTIME_SCHED = 0
    PERIODIC_SCHED = 1
