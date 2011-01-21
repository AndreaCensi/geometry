from . import LieGroup

class SpecialEuclidean(LieGroup):
    def __init__(self, n):
        LieGroup.__init__(self, n)
