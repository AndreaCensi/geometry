.. raw:: html
   :file: fork.html

.. include:: definitions.txt



PyGeometry
===========

|pygeometry| is a Python package that implements common operations on the differentiable manifolds usually encountered in computer vision and robotics.
Implemented manifolds: :math:`R^n`, :math:`S^n`,  :math:`SO(n)`, :math:`SE(n)`,
:math:`T(n)`.
Implemented operations: conversion between representations, geodesic distances, interpolation, random sampling.

The design goal is to have a set of well-tested primitives: I've been burned too many times from having used buggy functions. |pygeometry| is paranoid on program correctness. It uses PyContracts_ to validate input and return values. stochastic_testing_ (another experimental library) is used to check the correctness of the random sampling operations.

Download
--------

Use:

    pip install PyGeometry


.. raw:: html
   :file: download.html

Documentation
-------------

* :ref:`Manually written API description <api>`

* `Automatically generated API docs (epydoc)`__.

.. __: static/apidocs/index.html


Manifolds known by PyGeometry with embedding relations:

.. image:: static/manifolds.png

News
--------

2011-01-27: Started documentation.

2011 to 2018: Used in production in many projects.

2018-03-27: Refreshed documentation.

..
..     **Reference documentation**
..
..     * :ref:`creating_new_blocks`
..     * :ref:`running`
..     * :ref:`packaging`
..
..
..
..     **Block libraries documentation**
..
..     * :ref:`Included blocks <library>`
..
..     * Additional libraries (separate packages):
..
..       * procgraph_rawseeds_


.. raw:: html

   <div style='clear:both'></div>
