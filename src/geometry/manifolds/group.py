from abc import ABCMeta, abstractmethod


class Group(object):
    __metaclass__ = ABCMeta
    
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
        
    
    
