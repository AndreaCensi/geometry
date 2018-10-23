# coding=utf-8
from contracts import contract
from geometry.manifolds.differentiable_manifold import DifferentiableManifold
import numpy as np


# TODO: do some testing
class PointSet(object):
    """ A set of points on a differentiable manifold. """

    @contract(manifold=DifferentiableManifold)
    def __init__(self, manifold, points=[]):
        self.points = list(points)
        self.manifold = manifold

    def __len__(self):
        return len(self.points)

    def get_points(self):
        """ returns an iterable """
        return list(self.points)

    def add(self, p):
        self.points.append(p)

    def is_closer_than(self, p, min_dist):
        # quick check: check only last
        d_last = self.manifold.distance(p, self.points[-1])
        if d_last <= min_dist:
            return True
        return self.minimum_distance(p) <= min_dist

    def distances_to_point(self, p):
        return np.array([self.manifold.distance(p, p0) for p0 in self.points])

    def minimum_distance(self, p):
        dists = self.distances_to_point(p)
        return np.min(dists)

    def average(self):
        """ Returns the average point """
        # TODO: generalize
        return self.manifold.riemannian_mean(self.points)

    def closest_index_to(self, p):
        dists = self.distances_to_point(p)
        return np.argmin(dists)

    def centroid_index(self):
        avg = self.average()
        closest = self.closest_index_to(avg)
        return closest

    def centroid(self):
        """ REturns the point which is closest to the average """
        i = self.centroid_index()
        return self.points[i]

