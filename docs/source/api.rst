
.. py:currentmodule:: snp_geometry

.. py:module:: snp_geometry



Spheres
------------------

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


Rotations and quaternions
-------------------------
 
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


Poses
-------------------------------
.. autofunction:: pose_from_rotation_translation
.. autofunction:: rotation_translation_from_pose

.. autofunction:: extract_pieces
.. autofunction:: combine_pieces 


Contracts
---------------

These are some of the contracts defined using PyContracts_.

.. autofunction:: assert_orthogonal
.. autofunction:: unit_length
.. autofunction:: finite
.. autofunction:: orthogonal
.. autofunction:: rotation_matrix
.. autofunction:: skew_symmetric
.. autofunction:: directions


Misc utils
---------------
.. autofunction:: default_axis
.. autofunction:: default_axis_orthogonal
.. autofunction:: safe_arccos
.. autofunction:: normalize_pi
.. autofunction:: normalize_length
.. autofunction:: normalize_length_or_zero 
.. autofunction:: assert_allclose


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

Included manifolds
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
