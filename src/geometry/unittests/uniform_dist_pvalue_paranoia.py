# coding=utf-8
from scipy.stats.distributions import random_integers  #@UnresolvedImport

import numpy as np


def main():
    from  stochastic_testing import uniform_dist_pvalue  #@UnresolvedImport
    for N in [10, 100, 1000, 10000, 100000]:
        pvalues = np.empty(N)
        for i in range(N):
            dist = sample_uniform_dist(bins=5, N=100)
            pvalues[i] = uniform_dist_pvalue(dist)

        print('Testing with N = %d' % N)
        for pvalue in [0.5, 0.05, 0.01]:
            perc = (pvalues < pvalue).mean()
            print('- pvalue below %.3f: %.3f' % (pvalue, perc))


def sample_uniform_dist(bins, N):
    dist = np.zeros(bins)
    for x in random_integers(low=0, high=bins - 1, size=N):
        dist[x] += 1
    return dist


if __name__ == '__main__':
    main()

