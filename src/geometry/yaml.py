
import numpy as np
from geometry.manifolds import DifferentiableManifold
#
#def array_to_lists(x):
#    return x.tolist()
#
#def packet(space, rep, value):
#    return {'space': space, 'repr': rep, 'value': value}
#
#@contract(x='SE3')
#def yaml_from_SE3(x):
#    return packet('SE3', 'matrix', array_to_lists(x))
#
#@contract(x='se3')
#def yaml_from_se3(x):
#    return packet('se3', 'matrix', array_to_lists(x))
#    
## what about user-centered?
#def yaml_from_TSE3(x):
#    pose, vel = x    
#    return packet('TSE3', 'base-tangent',
#                  [yaml_from_SE3(pose), yaml_from_se3(vel)])


converters = {}
default_representation = {}


def register(manifold_name, representation, converter):
    if not manifold_name in default_representation:
        default_representation[manifold_name] = representation
    key = (manifold_name, representation)
    assert not key in converters
    converters[key] = converter


def get_default_representation(manifold):
    if isinstance(manifold, DifferentiableManifold):
        key = str(manifold)
    else:
        key = manifold

    if not key in default_representation:
        raise Exception('Cannot find representation for %s.' % manifold)

    return default_representation[key]


def to_yaml(manifold, value, representation=None):
    if representation is None:
        representation = get_default_representation(manifold)
    key = (manifold, representation)
    if not key in converters:
        raise ValueError('Unknown format %s; I know %s.' %
                         (key, converters.keys()))
    conv = converters[key]
    x = conv.to_yaml(value)
    return ['%s:%s' % (manifold, representation), x]


def from_yaml(x):
    if not isinstance(x, list):
        raise ValueError('I expect a list with two elements.')
    form = x[0]
    value = x[1]
    space, representation = form.split(':')

    key = (space, representation)
    if not key in converters:
        raise ValueError('Unknown format %s; I know %s.' %
                         (key, converters.keys()))
    conv = converters[key]
    return conv.from_yaml(value)


class Representation:
    def to_yaml(self, x):
        pass

    def from_yaml(self, y):
        pass


class SE3_m44(Representation):
    @staticmethod
    def to_yaml(x):
        return x.tolist()

    @staticmethod
    def from_yaml(y):
        return np.array(y)


class se3_m44(Representation):
    @staticmethod
    def to_yaml(x):
        return x.tolist()

    @staticmethod
    def from_yaml(y):
        return np.array(y)


class TSE3_bt(Representation):
    @staticmethod
    def to_yaml(x):
        a, b = x
        return [SE3_m44.to_yaml(a), se3_m44.to_yaml(b)]

    @staticmethod
    def from_yaml(y):
        return (from_yaml(y[0]), from_yaml(y[1]))

register('SE3', 'm44', SE3_m44)
register('TSE3', 'bt', TSE3_bt)
