import numpy as np
from scipy import special, stats


def poisson_beta_pmf(k, k_on, k_off, k_syn, n_roots=50):
    assert(k_on > 0)
    assert(k_off > 0)

    roots, weights = special.j_roots(n_roots, alpha=k_off - 1, beta=k_on - 1)
    mus = k_syn * (roots + 1) / 2
    assert(max(mus) < 1e6)

    gs = np.sum(weights * stats.poisson.pmf(k.reshape(-1, 1), mus), axis=1)
    probabilities = 1 / special.beta(k_on, k_off) * 2 ** (1 - k_on - k_off) * gs
    return probabilities
