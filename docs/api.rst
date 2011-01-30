.. include:: definitions.txt


.. _api_details:

PyGeometry API details
========================

.. py:module:: geometry
 
   
   
S(n) - Hyperspheres
----------------------


 
Random sampling
+++++++++++++++
.. autofunction:: random_direction
.. autofunction:: random_directions
.. autofunction:: any_distant_direction
.. autofunction:: any_orthogonal_direction
.. autofunction:: random_orthogonal_direction
.. autofunction:: random_directions_bounded

Misc
+++++++++++++++

.. autofunction:: geodesic_distance_on_sphere
.. autofunction:: distribution_radius
.. .. autofunction:: distances_from
.. autofunction:: sorted_directions

Manifolds objects
+++++++++++++++++++

.. autoclass:: Sphere
    :members:
    :undoc-members:

.. py:data:: S1

   Unit circle as a subset of :math:`R^2`.
    
.. py:data:: S2

   Unit sphere.
   

SO(n) - Rotations and quaternions
---------------------------------

    
    
Conversions
+++++++++++++++++++

.. autofunction:: geometry.rotations.hat_map
.. autofunction:: geometry.rotations.map_hat
.. autofunction:: geometry.rotations.rotation_from_quaternion
.. autofunction:: geometry.rotations.rotation_from_axis_angle
.. autofunction:: geometry.rotations.rotation_from_axis_angle2
.. autofunction:: geometry.rotations.axis_angle_from_quaternion
.. autofunction:: geometry.rotations.axis_angle_from_rotation
.. autofunction:: geometry.rotations.quaternion_from_rotation
.. autofunction:: geometry.rotations.quaternion_from_axis_angle

Random sampling
+++++++++++++++++++
.. autofunction:: geometry.random_geometry.random_quaternion
.. autofunction:: geometry.random_geometry.random_rotation
.. autofunction:: geometry.random_geometry.random_orthogonal_transform

Misc
+++++++++++++++++++
.. autofunction:: geodesic_distance_for_rotations



Manifolds objects
+++++++++++++++++

.. py:data:: SO2 
    
    Planar rotations.
    
.. py:data:: SO3 
    
    Rotations in 3D.
    
.. py:data:: so2 
    
    Lie algebra for planar rotations.

.. py:data:: so3 
    
    Lie algebra for 3D rotations.
    
    
SE(n) - Poses
-------------------------------



Conversions
+++++++++++
.. autofunction:: pose_from_rotation_translation
.. autofunction:: rotation_translation_from_pose


Misc
+++++++++++
.. autofunction:: extract_pieces
.. autofunction:: combine_pieces 


Manifold objects
++++++++++++++++


.. autoclass:: SE
    :members:
    :undoc-members:
    
.. autoclass:: se
    :members:
    :undoc-members:

:py:class:`SE`

.. py:data:: SE2 
    
    Poses in 2D.
    
.. py:data:: SE3 
    
    Poses in 3D.

:py:class:`se`

.. py:data:: se2 
    
    Lie algebra for SE(2).
    
.. py:data:: se3 
    
    Lie algebra for SE(3).
    
    

Procrustes analysis
-------------------------------
.. autofunction:: best_orthogonal_transform
.. autofunction:: closest_orthogonal_matrix



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



Tori
----------------------------

Manifold objects
++++++++++++++++++

.. py:data:: T1
    
    One dimensional torus, mapped onto :math:`[-\pi,\pi)`.
    
    Note that this is equivalent to the unit circle, but the representation
    is different: :py:data:`T1` uses "angles" while :py:data:`S2` uses unit vectors in
    :math:`R^2`.
    
.. py:data:: T2
    
    2D torus.
    
.. py:data:: T3
    
    3D torus.



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

.. autoclass:: Euclidean
    :members:
    :undoc-members:

.. autoclass:: SO
    :members:
    :undoc-members:


.. autoclass:: Torus
    :members:
    :undoc-members:

.. autoclass:: Moebius
    :members:
    :undoc-members:


