from unittest import main, TestCase

from vr import nearest_neighbors, lower_neighbors, expand_inductive, \
     incremental_vr

class VRTests(TestCase):
    def setUp(self):
        self.a, self.b, self.c = (0, 0), (1, 0), (0, 1)
        a, b, c = self.a, self.b, self.c
        self.points = [a, b, c]
        self.neighbors = [[a, b], [a, c], [c, b]]
        
    def test_nearest_neighbors(self):
        a, b, c = self.a, self.b, self.c
        ns = list(nearest_neighbors([a, b, c], .25))
        self.assertEqual(len(ns), 0)

        ns = list(nearest_neighbors([a, b, c], 1.4))
        self.assertEqual(len(ns), 2)

        ns = list(nearest_neighbors([a,b,c], 2.1))
        self.assertEqual(len(ns), 3)
        self.assertEqual(ns, [[a, b], [a, c], [c, b]])

    def test_lower_neighbors(self):
        a, b, c = self.a, self.b, self.c
        self.assertEqual(list(lower_neighbors(self.neighbors, a)), [])
        self.assertEqual(list(lower_neighbors(self.neighbors, c)), [a])
        self.assertEqual(list(lower_neighbors(self.neighbors, b)), [a, c])

    def test_expand_inductive(self):
        a, b, c = self.a, self.b, self.c
        sxs = expand_inductive(self.points, self.neighbors, 2)
        self.assertEqual(sxs[2], [[a, c, b]])

    def test_incremental_vr(self):
        a, b, c = self.a, self.b, self.c
        sxs = incremental_vr(self.points, self.neighbors, 2)
        self.assertEqual(sxs[2], [[a, c, b]])

    

        
if __name__ == '__main__':
    main()
