.. include:: definitions.txt


.. _api:

PyGeometry API
==============


Usage notes
-----------

* No fancy OO-overdose here. Geometric objects (rotation matrices, poses, etc.) are represented using vanilla 
  Numpy array: there's no class Rotation, Pose, etc. If you don't think this is a good
  idea, your mind has been spoiled by C++ or Java classes taught by clueless professors.


* The main procedures are implemented as simple functions accepting and returning numpy arrays.
  Manifolds are implemented using classes that wrap the simple functions.

* Manifolds objects "know" how to compute distances, interpolate, etc. This makes sense: for example, the interpolation between the identity and a rotation matrix depends on whether you are considering them as elements of *GL(n)* or *SO(n)*.
  
* Most functions declare contracts among parameters and return values using the PyContracts_ library. This is slightly paranoid. You can disable all those checks using  ``contracts.disable_all()``.
    
* The naming conventions for conversion operations is::

      x = <X>_from_<Y>(y)
    
  For example::
  
      R = rotation_from_axis_angle(axis, angle)
      axis, angle = axis_angle_from_rotation(R)
      R = rotation_from_quaternion(q)



.. d .. autosummary
.. 
..    geometry.geodesic_distance_on_sphere
..    geometry.distribution_radius


.. .. py:currentmodule:: geometry

.. py:module:: geometry
   
   
S(n) - Hyperspheres
------------

.. autofunction:: geodesic_distance_on_sphere
.. autofunction:: distribution_radius
.. autofunction:: distances_from
.. autofunction:: sorted_directions

Random sampling
+++++++++++++++
.. autofunction:: random_direction
.. autofunction:: random_directions
.. autofunction:: any_distant_direction
.. autofunction:: any_orthogonal_direction
.. autofunction:: random_orthogonal_direction
.. autofunction:: random_directions_bounded


SO(n) - Rotations and quaternions
---------------------------------
 
.. autofunction:: hat_map
.. autofunction:: map_hat
.. autofunction:: rotation_from_quaternion
.. autofunction:: rotation_from_axis_angle
.. autofunction:: rotation_from_axis_angle2
.. autofunction:: axis_angle_from_quaternion
.. autofunction:: axis_angle_from_rotation
.. autofunction:: quaternion_from_rotation
.. autofunction:: quaternion_from_axis_angle
.. autofunction:: geodesic_distance_for_rotations

Random sampling
+++++++++++++++++++
.. autofunction:: random_quaternion
.. autofunction:: random_rotation
.. autofunction:: random_orthogonal_transform


SE(n) - Poses
-------------------------------
.. autofunction:: pose_from_rotation_translation
.. autofunction:: rotation_translation_from_pose

.. autofunction:: extract_pieces
.. autofunction:: combine_pieces 



Misc utils
---------------

.. autofunction:: default_axis
.. autofunction:: default_axis_orthogonal
.. autofunction:: safe_arccos
.. autofunction:: normalize_pi
.. autofunction:: normalize_length
.. autofunction:: normalize_length_or_zero 
.. autofunction:: assert_allclose


These are some of the contracts defined using PyContracts_.

.. autofunction:: assert_orthogonal
.. autofunction:: unit_length
.. autofunction:: finite
.. autofunction:: orthogonal
.. autofunction:: rotation_matrix
.. autofunction:: skew_symmetric
.. autofunction:: directions



Manifolds and Matrix Lie Groups interface
-------------------------------------------------

.. autoclass:: DifferentiableManifold
    :members:
    :undoc-members:
.. autoclass:: Group
    :members:
    :undoc-members:
.. autoclass:: MatrixLieAlgebra
    :members:
    :undoc-members:
.. autoclass:: MatrixLieGroup
    :members:
    :undoc-members:

Included generic manifolds
----------------------------

.. autoclass:: Sphere
    :members:
    :undoc-members:
.. autoclass:: Euclidean
    :members:
    :undoc-members:
.. autoclass:: SO
    :members:
    :undoc-members:
.. autoclass:: SE
    :members:
    :undoc-members:
.. autoclass:: Torus
    :members:
    :undoc-members:
.. autoclass:: Moebius
    :members:
    :undoc-members:


Shortcuts
----------------------------

.. autodata:: E1
.. autodata:: E2
.. autodata:: S1
.. autodata:: S2
.. autodata:: SO2 
.. autodata:: SO3 
.. autodata:: so2 
.. autodata:: so3 
.. autodata:: SE2 
.. autodata:: SE3 
.. autodata:: se2 
.. autodata:: se3 
.. autodata:: T1
.. autodata:: T2
.. autodata:: T3

