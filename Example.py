import LineIntersection
# Example Call of the LineIntersection Algorithm

# The list of line Intersections should be of the format [((float, float), (float, float))]
# where each inner tuple represents the endpoints of a line segment
lns = [((6, 1), (6, 4.5)), ((1.5, 1.5), (9, 9)), ((1, 10), (10, 1)), ((3, 1.9), (2, 1)), ((1, 3), (3, 1)),
       ((4.1, 4), (6.9, 4)), ((5.5, 5.5), (6, 5.7)), ((4, 5.5), (5.5, 5.5))]

intersection_finder = LineIntersection.FindIntersections()

# The search_intersections method takes a list of line segments in the above format.
intersections = intersection_finder.search_intersections(lns)

# The algorithm returns the intersection points along with the associated line segments in the format [(Point, [Line])].
print([(intersection[0].x, intersection[0].y) for intersection in intersections])

