# markov.py
import numpy as np
from cache import AsyncLRU

@AsyncLRU(maxsize=128)
async def get_ideal_rolls(start, desired_p):
    tmat = await get_markov_tmat(start)

    init_progression = np.array([1 / start] * start, dtype=np.float16)

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
        row = np.array([0] * (i) + [1/(n-i)] * (n-i), dtype=np.float16)
        mat.append(row)

    return np.array(mat, dtype=np.float16)
