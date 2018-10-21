# coding=utf-8
from abc import abstractmethod
from contracts import ContractsMeta

__all__ = ['Group']


class Group(object):
    __metaclass__ = ContractsMeta

    @abstractmethod
    def multiply(self, g, h):
        ''' Implements the group operation. '''
        pass

    @abstractmethod
    def inverse(self, g):
        ''' Implements the group inversion. '''
        pass

    @abstractmethod
    def unity(self):
        ''' Returns the group unity. '''
        pass

    def identity(self):
        return self.unity()

