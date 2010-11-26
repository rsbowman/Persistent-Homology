import sys, time
from random import random
from math import sin, cos, pi

def sample_circle():
    return [cos(2*pi*random()), sin(2*pi*random())]

def sample_torus(dim):
    return tuple(sum((sample_circle() for i in range(dim + 1)), []))

from vr import nearest_neighbors, expand_inductive, incremental_vr

def time_everything(n_samples, dim, epsilon, max_dim):
    points = [sample_torus(dim) for i in range(n_samples)]

    now = time.time()
    one_skel = list(nearest_neighbors(points, epsilon))
    nn_time = time.time() - now

    now = time.time()
    #exp_ind = expand_inductive(points, one_skel, max_dim)
    exp_ind_time = time.time() - now

    now = time.time()
    inc_vr = incremental_vr(points, one_skel, max_dim)
    inc_vr_time = time.time() - now

    def sxs_size(d):
        for k in d:
            print '{0}: {1}'.format(k, len(d[k]))
            
    sxs_size(inc_vr)
    return (nn_time, exp_ind_time, inc_vr_time)

def vr(n_samples, dim, epsilon, max_dim):
    points = [sample_torus(dim) for i in range(n_samples)]
    one_skel = list(nearest_neighbors(points, epsilon))
    return incremental_vr(points, one_skel, max_dim)

def main_profile(argv):
    import cProfile
    n_samples = 30
    dim = 3
    epsilon = 12.0
    max_dim = 6
    cProfile.run('vr({n_samples}, {dim}, {epsilon}, {max_dim})'.format(**locals()),
                'vr.prof')
    
def main(argv):
    n_samples = 40
    dim = 3

    #profile(n_samples, dim, 12.0, 5)
    tup = time_everything(n_samples, dim, 12.0, 5)
    print tup
    
if __name__ == '__main__':
    main(sys.argv)
