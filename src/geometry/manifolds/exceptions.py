# coding=utf-8
from geometry.formatting import formatm


class DoesNotBelong(Exception):
    ''' Exception thrown when a point does not belong
        to a certain manifold *M*. '''

    def __init__(self, M, point, e, context=None):
        self.M = M
        self.point = point
        self.e = '%s' % e
        self.context = context

    def __str__(self):
        try:
            s = ''
            if self.context is not None:
                s += '%s\n' % self.context
            s += ('%s: The point does not belong here:\n%s' %
                  (self.M, formatm('p', self.point)))
            s += self.e
            return s
        except Exception as e:
            return "(%s) %s: %s" % (e, self.M, self.point)
