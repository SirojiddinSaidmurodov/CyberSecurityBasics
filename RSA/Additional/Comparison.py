import time

import matplotlib.pyplot as plt

from RSA.Additional import euclidean_algorithms
from RSA.Additional.quick_exp import exp_mod
from RSA.rsa import *


def greedy_solution(a, m):
    for num in range(1, m):
        if a * num % p == 1:
            return num


def eyler(a, m):
    return exp_mod(a, m - 1, m)


interval = 500
time1 = []
time2 = []
time3 = []
for i in range(4, interval):
    print(i / interval * 100)
    p = get_random_prime_number(i)
    a = get_random_mutually_prime_number(p)
    # start = time.time()
    # greedy_solution(a, p)
    # end = time.time()
    # time1.append(end - start)
    start = time.time()
    eyler(a, p)
    end = time.time()
    time2.append(end - start)
    start = time.time()
    euclidean_algorithms.PAE(a, p)
    end = time.time()
    time3.append(end - start)

# plt.plot(range(4, interval), time1, label="greedy")
plt.plot(range(4, interval), time2, label="eyler")
plt.plot(range(4, interval), time3, label="PAE")
plt.legend()
plt.show()
