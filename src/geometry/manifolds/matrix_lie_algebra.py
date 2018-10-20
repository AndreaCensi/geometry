# coding=utf-8
from abc import abstractmethod

from contracts import contract
from .matrix_linear_space import MatrixLinearSpace

__all__ = ['MatrixLieAlgebra']


class MatrixLieAlgebra(MatrixLinearSpace):
    ''' This is the base class for Matrix Lie Algebra.

        It is understood that it is composed by square matrices.

        The only function that *has* to be implemented is the
        :py:func:`project` function that projects a square matrix
        onto the algebra. This function is used both for checking
        that a vector is in the algebra (see :py:func:`belongs`)
        and to mitigate the numerical errors.

        You probably also want to implement :py:func:`norm` if
        the default is not what you want.
    '''

    def __init__(self, n, dimension):
        MatrixLinearSpace.__init__(self, dimension=dimension,
                                   shape=(n, n))
        self.n = n

    @abstractmethod
    @contract(a='belongs', returns='array[K]')
    def vector_from_algebra(self, a):
        ''' Isomorphism from elements of the algebra to vectors.
        (For example, so(3) <==> R^3).
         '''
        # raise ValueError('Not implemented for %s.' % self)

    @abstractmethod
    @contract(returns='belongs', v='array[K]')
    def algebra_from_vector(self, v):
        ''' Isomorphism from elements of the algebra to vectors.
        (For example, so(3) <==> R^3).
         '''
        # raise ValueError('Not implemented for %s.' % self)

    # TODO: bracket
