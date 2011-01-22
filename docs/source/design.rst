

Design goals
============

* Group together most common geometric operations needed in robotics.

* Designed to be trustful. Everything is carefully checked.
  Translation: this is slow by design. 

* Not designed to be maximally general: everything is real, not complex, etc.



Design notes
============

* The functionality is divided in two subgroups. Everything with a function, then a OO.

  (This is so you can copy and paste the code if you want)
  
* No fancy OO-overdose. Objects (rotation matrices, poses, etc.) are represented using
  Numpy array. There's no class Rotation, Pose, etc. If you don't think this is a good
  idea, your mind has been spoiled by C++ or Java classes taught by clueless professors.

* Uses the PyContracts_ library for defining contracts. You can disable all its checks
    using ``disable_all()``.
    
* Naming conventions:

    x = <X>_from_<Y>(y)
    
  For example:
  
    R = rotation_from_axis_angle(axis, angle)
    axis, angle = axis_angle_from_rotation(R)
    R = rotation_from_quaternion(q)

Minor
-----

* ``belongs`` throws an exception because you usually want to know *why*
    the points
    
    
    
References
==========

Fiori

Smith



.. _PyContracts: http://andreacensi.github.com/contracts/
