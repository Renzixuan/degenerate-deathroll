# markov.py
import numpy as np
from functools import lru_cache

@lru_cache(maxsize=256)
async def get_ideal_rolls(start, desired_p):
    tmat = await get_markov_tmat(start)

    init_progression = np.array([1 / start] * start)

    p = init_progression[-1]
    roll_count = 0

    while p < desired_p:
        roll_count = roll_count + 1

        init_progression = np.matmul(init_progression, tmat)
        p = init_progression[-1]

    return roll_count + 1

async def get_markov_tmat(n):
    mat = []
    for i in range(n):
        row = [0] * (i) + [1/(n-i)] * (n-i)
        mat.append(row)

    return np.array(mat)
