import math

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # collinear
    return 1 if val > 0 else 2  # 1 for clockwise, 2 for counterclockwise

def convex_hull(points):
    n = len(points)
    if n < 3:
        return []

    hull = []

    l = min(points, key=lambda x: x[0])
    p = l
    q = None
    while True:
        hull.append(p)
        q = points[0]
        for i in range(1, n):
            if q == p or orientation(p, points[i], q) == 2:
                q = points[i]
        p = q
        if p == l:
            break

    return hull

def insertion_heuristic_convex_hull(points):
    hull = convex_hull(points)
    unvisited = set(points)
    for point in hull:
        unvisited.remove(point)

    path = hull
    while unvisited:
        min_dist = float('inf')
        insert_point = None
        for candidate in unvisited:
            for i in range(1, len(path)):
                dist = distance(path[i - 1], candidate) + distance(candidate, path[i]) - distance(path[i - 1], path[i])
                if dist < min_dist:
                    min_dist = dist
                    insert_point = (candidate, i)
        path.insert(insert_point[1], insert_point[0])
        unvisited.remove(insert_point[0])

    tour = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    return tour
