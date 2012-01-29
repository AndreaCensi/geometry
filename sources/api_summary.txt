.. include:: definitions.txt


.. _api:


PyGeometry API
========================


Design notes
-----------------

* No fancy OO-overdose here. Geometric objects (rotation matrices, poses, etc.) are represented using vanilla 
  Numpy array: there's no class Rotation, Pose, etc. If you don't think this is a good
  idea, your mind has been spoiled by C++ or Java classes taught by clueless professors.


* The main procedures are implemented as simple functions accepting and returning numpy arrays.
  Manifolds are implemented using classes that wrap the simple functions.

* Manifolds objects "know" how to compute distances, interpolate, etc. This makes sense: for example, the interpolation between the identity and a rotation matrix depends on whether you are considering them as elements of *GL(n)* or *SO(n)*.
  
* Most functions declare contracts among parameters and return values using the PyContracts_ library. This is slightly paranoid. You can disable all those checks using  ``contracts.disable_all()``.


Namespace
++++++++++++++++++

Every symbol is imported in the ``geometry`` module.

However, in this API documentation, the full path to the module is shown. For example, ``rotation_from_axis_angle`` is defined in the module ``geometry.rotations``, but you can import it as such: ::

    from geometry import rotation_from_axis_angle

In fact, this will import all functions and classes: ::

    from geometry import *


Naming conventions
++++++++++++++++++
    
The naming conventions for conversion operations is::

    x = <X>_from_<Y>(y)

For example: ::

    R = rotation_from_axis_angle(axis, angle)
    axis, angle = axis_angle_from_rotation(R)
    R = rotation_from_quaternion(q)



Manifolds interface 
-------------------------------------------------

.. autosummary::  
   :toctree: api
   
    geometry.manifolds.base.DifferentiableManifold
    geometry.manifolds.base.Group
    geometry.manifolds.matrix_lie_group.MatrixLieAlgebra
    geometry.manifolds.matrix_lie_group.MatrixLieGroup
    

Hyperspheres
------------

Manifold class:

.. autosummary::
   :toctree: api

    geometry.manifolds.sphere.Sphere
    
Instances of the manifold class: 

.. py:data:: geometry.manifolds.S1 
    
    S1: Unit circle (2D vectors of norm 1).
    
.. py:data:: geometry.manifolds.S2 
    
    S2: Unit sphere (3D vectors of norm 1)
    
 
Contracts (PyContracts_) and checks:

.. autosummary::
   :toctree: api

    geometry.spheres.assert_orthogonal
    geometry.spheres.unit_length
    geometry.spheres.directions


Random sampling:

.. autosummary::
   :toctree: api

    geometry.spheres.random_direction
    geometry.spheres.random_directions
    geometry.spheres.any_distant_direction
    geometry.spheres.any_orthogonal_direction
    geometry.spheres.random_orthogonal_direction
    geometry.spheres.random_directions_bounded

Miscellaneous:

.. autosummary::
   :toctree: api

    geometry.spheres.geodesic_distance_on_sphere
    geometry.spheres.distribution_radius
    geometry.spheres.distances_from
    geometry.spheres.sorted_directions



SO(n) -- rotations
--------------------

Manifold classes:

.. autosummary::
   :toctree: api

    geometry.manifolds.special_orthogonal.SO
    geometry.manifolds.special_orthogonal.so

Instances:

.. py:data:: geometry.manifolds.SO2 
    
    SO(2): 2x2 rotation matrices
    
.. py:data:: geometry.manifolds.SO3 
    
    SO(3): 3x3 rotation matrices
    
.. py:data:: geometry.manifolds.so2 
    
    Lie algebra for SO(2): 2x2 skew-symmetric matrices
    
.. py:data:: geometry.manifolds.so3 
    
    Lie algebra for SO(3): 3x3 skew-symmetric matrices
    
    
    
Contracts and checks:

.. autosummary::
   :toctree: api

    geometry.rotations.rotation_matrix
    geometry.rotations.skew_symmetric
    geometry.rotations.orthogonal

Conversions functions:

.. autosummary::
   :toctree: api

    geometry.rotations.hat_map
    geometry.rotations.map_hat
    geometry.rotations.rotation_from_quaternion
    geometry.rotations.rotation_from_axis_angle
    geometry.rotations.rotation_from_axis_angle2
    geometry.rotations.axis_angle_from_quaternion
    geometry.rotations.axis_angle_from_rotation
    geometry.rotations.quaternion_from_rotation
    geometry.rotations.quaternion_from_axis_angle

Random sampling:

.. autosummary::
   :toctree: api

    geometry.rotations.random_quaternion
    geometry.rotations.random_rotation
    geometry.rotations.random_orthogonal_transform
    
Random sampling:

.. autosummary::
   :toctree: api

   geometry.rotations.geodesic_distance_for_rotations
   
   
   
   
SE(n) -- poses
--------------------

Manifold classes:

.. autosummary::
   :toctree: api

    geometry.manifolds.special_euclidean.SE
    geometry.manifolds.special_euclidean.se

Instances:


.. py:data:: geometry.manifolds.SE2 
    
    SE(2): 2D poses
    
.. py:data:: geometry.manifolds.SE3 
    
    SE(3): 3D poses
    
.. py:data:: geometry.manifolds.se2 
    
    Lie algebra for SE(2).
    
.. py:data:: geometry.manifolds.se3 
    
    Lie algebra for SE(3).
    
    
Conversions:

.. autosummary::
   :toctree: api

    geometry.poses.pose_from_rotation_translation
    geometry.poses.rotation_translation_from_pose
    geometry.poses.SE2_from_translation_angle
    geometry.poses.translation_angle_from_SE2
    geometry.poses.SE2_from_xytheta
    geometry.poses.se2_from_linear_angular
    geometry.poses.linear_angular_from_se2

Misc:

.. autosummary::
   :toctree: api

    geometry.poses.extract_pieces
    geometry.poses.combine_pieces 


    
    
Procrustes analysis
-------------------------------

.. autosummary::
   :toctree: api

    geometry.procrustes.best_orthogonal_transform
    geometry.procrustes.closest_orthogonal_matrix

    

Basic utils
---------------

.. autosummary::
   :toctree: api
    
    geometry.basic_utils.assert_allclose
    geometry.basic_utils.normalize_length
    geometry.basic_utils.normalize_length_or_zero
    geometry.basic_utils.safe_arccos
    geometry.basic_utils.finite
    


    
    
Other manifolds
----------------------------

.. autosummary:: 
   :toctree: api

    geometry.manifolds.euclidean.Euclidean
    geometry.manifolds.torus.Torus
    geometry.manifolds.moebius.Moebius
    

