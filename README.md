# LineIntersection

LineIntersection.py contains the necessary Classes and Functions to find all intersection points
of a list of 2D line segments with a runtime of nlog(n), using a sweepline based approach. 

The algorithm was adapted from:
Computational Geometry: Algorithms and Applications, Third Edition by de Berg, Cheong, Kreveld and Overmars
pages 25 - 27

This script accepts a list lines in form of tuples of two dimensional cartesian points,
which are given as tuples,
i.e. [((6, 1), (6, 4.5)), ((1.5, 1.5), (9, 9)), ((1, 10), (10, 1)), ((3, 1.9), (2, 1)), ((1, 3), (3, 1))]

The script contains classes to Represent Points, Lines and the Sweepline in addition to the class containing
the methods for the calculations.

This script uses a custom AVL-Tree implementation, contained in AVLTree.py, that needs to be installed for it
to function. In addition to that numpy needs to be installed to run the script.

A example call of the Algorithm can be found in  Example.py
