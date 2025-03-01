from typing import Self
import AVLTree
import numpy as np
import math
"""
Line Intersection Script
This Script contains the necessary Classes and Functions to find all intersection points
of a list of 2D line segments with a runtime of nlog(n), using a sweepline based approach. 

The algorithm was adapted from:
Computational Geometry: Algorithms and Applications, Third Edition by de Berg, Cheong, Kreveld and Overmars
pages 25 - 27

This script uses a custom AVL-Tree implementation that (delivered alongside this script) needs to be installed for it
to function. In addition to that numpy needs to be installed to run the script.

This script accepts a list lines in form of tuples of teo dimensional cartesian points,
which are given as tuples,
i.e. [((6, 1), (6, 4.5)), ((1.5, 1.5), (9, 9)), ((1, 10), (10, 1)), ((3, 1.9), (2, 1)), ((1, 3), (3, 1))]

The script contains classes to Represent Points, Lines and the Sweepline in addition to the class containing
the methods for the calculations. 
"""


class Sweepline:
    """
    Representation of the sweepline
    centrally saves the current y-position of the sweepline, allowing for direct access from each line segment,
    and the FindIntersections Class

    Attributes:
    ----------
    sweepline_position : number
        current y-position of the sweepline in a cartesian coordinate system
    """

    def __init__(self, position: float):
        """
        :param position: float
            initial y-position of the sweepline
        """
        self.sweepline_position = position


class Point:
    """
    Representation of a 2D point for use of the FindIntersections class
    Attributes:
    -----------
    line_segment: Line
        line segment the point is part of. This is required for the algorithm.
    x: float
        x position of the point on a cartesian coordinate system
    y: float
        y position of the point on a cartesian coordinate system

    Methods:
    -------
        compare(point : Point): bool
        checks whether the position of point is identical to own position
    """
    line_segment = None

    def __init__(self, x_position: float, y_position: float):
        """
        Initializes a new point
        :param x_position: float
            x position of the point on a cartesian coordinate system
        :param y_position: float
            y position of the point on a cartesian coordinate system
        """
        self.x = x_position
        self.y = y_position

    def compare(self, point: Self) -> bool:
        """
        Compares the parent object to another point to determine whether their position is identical
        :param point: Point
            another point the object should be compared to.
        :return: bool:
            True if the position of both points is identical; False if not
        """
        return self.x == point.x and self.y == point.y


class Line:
    """
    Representation of a single line segment f or the use of the FindIntersections Class
    Attributes:
    ----------
    upper: Point
        endpoint of the line segment with the higher y-coordinate, if the coordinate is the same the pont with the
        smaller x-coordinate is chosen
    lower: Point
        endpoint of the line segment with the lower y-coordinate, if the coordinate is the same the pont with the
        greater x-coordinate is chosen
    sweepline: Sweepline
        The sweepline object used as the sweepline by FindIntersections
    order: float
        The x coordinate of the line on the current sweepline. Required for sorting in the FindIntersections class
    """
    def __init__(self, point1: Point, point2: Point, sweepline: Sweepline):
        """
        Initializes a new Line Segment by assigning an upper and lower point based on the y-coordinates of the points
        :param point1: Point
            Endpoint of the Line Segment
        :param point2: Point
            Endpoint of the Line Segment
        :param sweepline: Sweepline
            The Sweepline used in FindIntersections
        """
        if point1.y > point2.y:
            self.upper = point1
            self.lower = point2
        elif point1.y < point2.y:
            self.upper = point2
            self.lower = point1
        else:
            if point1.x < point2.x:
                self.upper = point1
                self.lower = point2
            else:
                self.upper = point2
                self.lower = point1
        self.sweepline = sweepline
        self.upper.line_segment = self
        self.order = 0.0


class FindIntersections:
    """
    This class contains the Methods to find all intersection points of a set of 2D line segments. By calling the method
    search_intersections() with the line segments as alist of tuples of points the intersections are calculated and
    returned as a list of intersection points along with the according line segments.
    Example call: search_intersections(((6, 1), (6, 4.5)), ((1.5, 1.5), (9, 9)), ((1, 10), (10, 1)))

    Attributes:
    ----------
        status_structure: AvlTree
            data structure containing line segments currently intersected by the sweepline in ascending order of
            x-coordinate of intersection point
        event_queue: AvlTree
            data structure containing all potential intersection points
        sweepline: Sweepline
            the current sweepline used by the algorithm to detect intersections

    Methods:
    --------
            search_intersections(lines: [((float, float), (float, float))]): list
                primary method to find intersections from a list of line segments. The lines must be given as a list
                of tuples each containing the two endpoints as tuples of floats.
            line_factory(lines: [((float, float), (float, float))], sweepline: Sweepline): [Line]
                converts the initial list of line segments to a list  of "Line"-objects for the use of the algorithm.
            event_point_factory(lines: [((float, float), (float, float))]): [Point]
                creates a list of event points as "Point"-objects from the initial list of line segments.
            find_intersections(line_segments: list, event_points: [Point]): list
                main loop of the line intersection algorithm works through all potential intersection points saved in the
                event queue.
            handle_event_points(event_point: Point, line_segments: list, intersection_list: list): list
                checks for each point in the event queue whether it is an intersection point between two or more line
                segments in the status structure
            find_new_event(self, left_segment: Line, right_segment: Line, point: Point): None
                finds new potential intersection points from the provided line segments, and adds them
                to the event queue.
            line_intersection(self, segment1: Line, segment2: Line): tuple
                finds the intersection point between segment1 and segment2 if it exists.
            compare_events(key1: Point, key2: Point): bool
                determines the order of key1 and key2 with respect to their x and y coordinates.
            calculate_line_status_key(line: Line): float
                calculates the x-coordinate of line on the current sweepline position.
            calculate_line_status(line: Line, position: float): float
                calculates the x-coordinate of line for the y-coordinate "position".
            event_equals(key1: Point, key2: Point): bool
                checks whether two points have the same x and y-coordinates. Used as to check for equality in the
                event queue.
            lies_on_segment(segment: Line, point: Point): bool
                checks whether the point "point" is intersected by the line segment "segment".
            sort_by_sweepline_order(segments: [Line]): [Line]
                sorts a list of line segments in ascending order of the x-coordinate of their intersection point with
                 the sweepline.
    """
    status_structure = None
    event_queue = None
    sweepline: Sweepline

    def search_intersections(self, lines: [((float, float), (float, float))]) -> list:
        """
        primary method to find intersections from a list of line segments. The lines must be given as a list
        of tuples each containing the two endpoints as tuples of floats.
        :param lines: [((float, float), (float, float))]
         list of line segments as tuples of points, represented as tuples of floats
        :return: [(Point,[Line])]
         list of tuples intersection points as Point-objects, together with a list of the associated
         line segments as Line-objects
        """
        self.sweepline = Sweepline(position=0)
        return self.find_intersections(line_segments=self.line_factory(lines=lines, sweepline=self.sweepline),
                                       event_points=self.event_point_factory(lines=lines))

    @staticmethod
    def line_factory(lines: [((float, float), (float, float))], sweepline: Sweepline) -> [Line]:
        """
        converts the initial list of line segments to a list  of "Line"-objects for the use of the algorithm.
        :param lines: [((float, float), (float, float))]
            list of line segments to be converted as tuples of points, represented as tuples of floats
        :param sweepline: Sweepline
            the sweepline used in the algorithm
        :return: [Line]
            the line segments as a list of Line-objects
        """
        line_segments = []
        for line in lines:
            p1 = Point(line[0][0], line[0][1])
            p2 = Point(line[1][0], line[1][1])
            line_segments.append(Line(point1=p1, point2=p2, sweepline=sweepline))
        return line_segments

    @staticmethod
    def event_point_factory(lines: [((float, float), (float, float))]) -> [Point]:
        """
        creates a list of event points as "Point"-objects from the initial list of line segments.
        :param lines: [((float, float), (float, float))]
            list of line segments to be converted as tuples of points, represented as tuples of floats
        :return: [Point]
            The event points determined from the provided line segments
        """
        event_points = list({(line[0][0], line[0][1]) for line in lines}.union({(line[1][0], line[1][1])
                                                                                for line in lines}))
        return [Point(x_position=event_point[0], y_position=event_point[1]) for event_point in event_points]

    def find_intersections(self, line_segments: [Line], event_points: [Point]) -> list:
        """
        main loop of the line intersection algorithm works through all potential intersection points saved in the
        event queue.
        :param line_segments: [Line]
            all line segments to be checked for intersections.
        :param event_points: [Point]
            initial list of potential intersection points.
        :return: [(Point,[Line])]
            list of tuples intersection points as Point-objects, together with a list of the associated
            line segments as Line-objects
        """
        intersections = []
        self.event_queue = AVLTree.AvlTree(elements=[(event_point, event_point) for event_point in event_points],
                                           comparator=self.compare_events, equals=self.event_equals)
        self.status_structure = AVLTree.AvlTree(elements=[], comparator=None, equals=None)
        while self.event_queue.root is not None:
            next_event_point = self.event_queue.pop_lowest()
            self.handle_event_points(event_point=next_event_point, line_segments=line_segments,
                                     intersection_list=intersections)
        return intersections

    def handle_event_points(self, event_point: Point, line_segments: [Line], intersection_list: list) -> list:
        """
        Checks for each point in the event queue whether it is an intersection point between two or more line
        segments in the status structure.
        :param event_point: Point
            the event point which is checked for intersections between line segments.
        :param line_segments: [List]
            list of line segments which may or may not contain the event point.
        :param intersection_list:  [(Point,[Line])]
            list of detected intersection points with their associated line segments.
        :return: [(Point,[Line])]
            list of detected intersection points with their associated line segments updated for intersections on the
            current event point.
        """
        self.sweepline.sweepline_position = event_point.y
        ordered_segments = self.status_structure.pop_all()
        self.status_structure.insert_list([(self.calculate_line_status_key(line=segment), segment)
                                           for segment in ordered_segments])
        lower_p = []
        upper_p = []
        contains_p = []
        for segment in line_segments:
            if segment.upper.compare(event_point):
                upper_p.append(segment)
            elif segment.lower.compare(event_point):
                lower_p.append(segment)
                self.status_structure.remove_pair(self.calculate_line_status_key(line=segment), segment)
            elif self.lies_on_segment(segment=segment, point=event_point):
                contains_p.append(segment)
                self.status_structure.remove_pair(self.calculate_line_status_key(line=segment), segment)
        self.sweepline.sweepline_position -= 0.01
        upper_contains_p = self.sort_by_sweepline_order(segments=upper_p + contains_p)
        self.status_structure.insert_list([(segment.order, segment)
                                           for segment in upper_contains_p])
        potential_segments = upper_contains_p + lower_p
        if len(potential_segments) > 1:
            intersection_list.append((event_point, potential_segments))
        if (upper_p + contains_p).__len__() == 0:
            left_segment, right_segment = self.status_structure.find_neighbors(event_point.x)
            if left_segment and right_segment is not None:
                self.find_new_event(left_segment=left_segment, right_segment=right_segment, point=event_point)
        else:
            leftmost_segment = upper_contains_p[0]
            leftmost_point = leftmost_segment.upper.x
            rightmost_segment = upper_contains_p[0]
            rightmost_point = rightmost_segment.upper.x
            for segment in upper_p:
                if segment.upper.x < leftmost_point:
                    leftmost_segment = segment
                    leftmost_point = segment.upper.x
                if segment.upper.x > rightmost_point:
                    rightmost_segment = segment
                    rightmost_point = segment.upper.x
            for segment in contains_p:
                x = self.calculate_line_status_key(line=segment)
                if x < leftmost_point:
                    leftmost_segment = segment
                    leftmost_point = x
                if x > rightmost_point:
                    rightmost_segment = segment
                    rightmost_point = x
            left_neighbor = self.status_structure.find_left_neighbor_by_pair(self.calculate_line_status_key(
                line=leftmost_segment), leftmost_segment)
            if left_neighbor is not None and left_neighbor is not leftmost_segment:
                self.find_new_event(left_segment=left_neighbor, right_segment=leftmost_segment, point=event_point)
            right_neighbor = self.status_structure.find_right_neighbor_by_pair(
                self.calculate_line_status_key(line=rightmost_segment), rightmost_segment)
            if right_neighbor is not None and right_neighbor is not rightmost_segment:
                self.find_new_event(left_segment=right_neighbor, right_segment=rightmost_segment, point=event_point)
        self.sweepline.sweepline_position = event_point.y
        return intersection_list

    def find_new_event(self, left_segment: Line, right_segment: Line, point: Point) -> None:
        """
            finds new potential intersection points from the provided line segments, and adds them
            to the event queue.
        :param left_segment: Line
            line segment which is to be checked for potential intersections with other segments.
        :param right_segment: Line
            line segment which is to be checked for potential intersections with other segments.
        :param point: Point
            the current event point
        :return: Nothing
        """
        intersection = self.line_intersection(segment1=left_segment, segment2=right_segment)
        if intersection is not None and (intersection[1] < point.y
           or ((intersection[1] == point.y) and intersection[0] > point.x)):
            intersection_point = Point(intersection[0], intersection[1])
            if not self.event_queue.is_in(intersection_point):
                self.event_queue.insert((intersection_point, intersection_point))

    @staticmethod
    def compare_events(key1: Point, key2: Point) -> bool:
        """
        Comparator method for two Point objects to be used by the event queue.
        :param key1: Point
            point-object to be compared to another.
        :param key2: Point
            point-object to be compared to another.
        :return: bool
            true if the point with key1 should come before key2 in the event queue; false otherwise
        """
        if key1.y == key2.y:
            return key1.x < key2.x
        else:
            return key1.y > key2.y

    @staticmethod
    def calculate_line_status_key(line: Line) -> float:
        """
        calculates the x-coordinate of line on the current sweepline position.
        :param line: Line
            The Line for which the x-coordinate on the sweepline is required
        :return: float
            x-coordinate of line on the current sweepline position.
        """
        if line.lower.x == line.upper.x:
            return line.upper.x
        if line.lower.y == line.upper.y:
            return line.upper.x
        m = np.divide(line.upper.y - line.lower.y, line.upper.x - line.lower.x)
        b = line.upper.y - np.multiply(line.upper.x, m)
        return np.divide(line.sweepline.sweepline_position - b, m)

    @staticmethod
    def calculate_line_status(line: Line, position: float) -> float:
        """
        calculates the x-coordinate of line for any given y-coordinate.
        :param line: Line
            The Line for which the x-coordinate is required
        :param position: float
            The y-coordinate for which a x-coordinate is required
        :return: float
            the x-coordinate for the line
        """
        m = np.divide(line.upper.y - line.lower.y, line.upper.x - line.lower.x)
        b = line.upper.y - np.multiply(line.upper.x, m)
        return np.divide(position - b, m)

    @staticmethod
    def event_equals(key1: Point, key2: Point) -> bool:
        """
         checks whether two points have the same x and y-coordinates. Used as to check for equality in the event queue.
        :param key1: Point
            Point-object to be checked for equality.
        :param key2:
            Point-object to be checked for equality.
        :return: bool
            True if the two points are equal; False if not.
        """
        return key1.x == key2.x and key1.y == key2.y

    @staticmethod
    def lies_on_segment(segment: Line, point: Point) -> bool:
        """
        checks whether a given point is intersected by the given line segment.
        :param segment: Line
            the segment to be checked for intersection.
        :param point: Point
            the point to be checked for intersection.
        :return: bool
            True if the point is intersected by the line segment; False if not.
        """
        if point.y < segment.lower.y or point.y > segment.upper.y:
            return False
        rightmost_point = segment.upper
        leftmost_point = segment.lower
        if segment.lower.x > rightmost_point.x:
            rightmost_point = segment.lower
            leftmost_point = segment.upper
        if point.x < leftmost_point.x or point.x > rightmost_point.x:
            return False
        direction_x = segment.upper.x - segment.lower.x
        direction_y = segment.upper.y - segment.lower.y
        point_vector_x = point.x - segment.lower.x
        point_vector_y = point.y - segment.lower.y
        if direction_x == 0 and direction_y == 0:
            return False
        elif direction_x == 0:
            return point_vector_x == 0
        elif direction_y == 0:
            return point_vector_y == 0
        return math.isclose(point_vector_x / direction_x, point_vector_y / direction_y)

    def line_intersection(self, segment1: Line, segment2: Line) -> tuple:
        """
        finds the intersection point between segment1 and segment2 if it exists.
        :param segment1: Line
            Line segment to be checked for intersection.
        :param segment2: Line
            Line segment to be checked for intersection.
        :return: tuple
            The intersection point if the lines intersect, None if not
        """
        p1 = (segment1.lower.x, segment1.lower.y)
        v1 = (segment1.upper.x - segment1.lower.x, segment1.upper.y - segment1.lower.y)
        p2 = (segment2.lower.x, segment2.lower.y)
        v2 = (segment2.upper.x - segment2.lower.x, segment2.upper.y - segment2.lower.y)

        v2 = (v2[0] * -1, v2[1] * -1)
        np.transpose(np.array([v1, v2]))
        matrix = np.transpose(np.array([v1, v2]))
        rhs = np.array(p2) - np.array(p1)
        try:
            t, s = np.linalg.solve(matrix, rhs)
            intersection_point = np.array(p1) + t * np.array(v1)
            point = Point(intersection_point[0], intersection_point[1])
            if self.lies_on_segment(segment=segment1, point=point) and self.lies_on_segment(segment2, point):
                return tuple(intersection_point)
        except np.linalg.LinAlgError:
            return None, None

    def sort_by_sweepline_order(self, segments: [Line]) -> [Line]:
        """
        sorts a list of line segments in ascending order of the x-coordinate of their intersection point with
        the sweepline. Horizontal segments are always last in the list.
        :param segments: [Line]
            Unsorted list of line segments to be sorted.
        :return: [Line]
            sorted list of line segments.
        """
        if not segments:
            return segments
        sweepline_y = segments[0].sweepline.sweepline_position
        horizontals = [segment for segment in segments if segment.upper.y == segment.lower.y]
        segments = list(set(segments) - set(horizontals))
        verticals = [segment for segment in segments if segment.upper.x == segment.lower.x]
        segments = list(set(segments) - set(verticals))
        for segment in verticals:
            segment.order = segment.upper.x
        for segment in segments:
            segment.order = self.calculate_line_status(line=segment, position=sweepline_y)
        segments += verticals
        segments.sort(key=lambda x: x.order)
        if len(horizontals) > 0:
            for segment in horizontals:
                if len(segments) > 0:
                    segment.order = segments[-1].order + 0.01
                else:
                    segment.order = segment.upper.x
        return segments + horizontals
