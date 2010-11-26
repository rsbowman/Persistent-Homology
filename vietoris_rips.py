from math import sqrt

def euclidean_distance(x_tup, y_tup):
    return sum([(x-y)**2 for x, y in zip(x_tup, y_tup)])

def nearest_neighbors(points, epsilon, d=euclidean_distance):
    for i, p in enumerate(points):
        for p2 in points[i + 1:]:
            if d(p, p2) < epsilon:
                yield sorted([p, p2])

class LowerNeighbors(object):
    def __init__(self, neighbors):
        self.neighbors = neighbors
        self.cache = {}
        
    def __call__(self, point):
        if point in self.cache:
            return self.cache[point]
        nbs = set(lower_neighbors(self.neighbors, point))
        self.cache[point] = nbs
        return nbs
    
def lower_neighbors(neighbors, point):
    for pair in neighbors:
        if point in pair and pair.index(point) == 1:
            yield pair[0]

def make_lower_neighbors(neighbors, points):
    nbs = {}
    for point in points:
        nbs[point] = set(lower_neighbors(neighbors, point))
    return nbs

def expand_inductive(points, neighbors, max_dimension):
    simplices = {0: points,
                 1: neighbors}
    for i in range(1, max_dimension + 1):
        simplices[i + 1] = []
        for tau in simplices[i]:
            lns = [set(lower_neighbors(neighbors, u)) for u in tau]
            N = set.intersection(*lns)
            for v in N:
                simplices[i + 1].append(sorted(tau + [v]))
    return simplices

def cofaces(points, neighbors, max_dimension, tau, N,
            lower_neighbors):
    if len(tau) >= max_dimension + 2:
        return [tau]

    to_return = [tau]
    for v in N:
        sigma = tau + [v]
        M = set.intersection(N, lower_neighbors(v))
        to_return.extend(cofaces(points, neighbors, max_dimension,
                                 sigma, M, lower_neighbors))
    return to_return

def incremental_vr(points, neighbors, max_dimension):
    simplices = dict((i, []) for i in range(max_dimension + 2))
    lower_neighbors = LowerNeighbors(neighbors)
    for u in points:
        N = lower_neighbors(u)
        cfs = cofaces(points, neighbors, max_dimension, [u], N,
                      lower_neighbors)
        for face in cfs:
            simplices[len(face) - 1].append(sorted(face))
    return simplices
