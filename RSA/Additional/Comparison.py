import time

import matplotlib.pyplot as plt

from RSA.Additional import euclidean_algorithms
from RSA.Additional.quick_exp import exp_mod
from RSA.rsa import *


def brutforce(a, m):
    for num in range(1, m):
        if a * num % p == 1:
            return num


def eyler(a, m):
    return exp_mod(a, m - 1, m)


interval = 250
time1 = []
time2 = []
time3 = []
for i in range(4, interval):
    print(i / interval * 100)
    p = get_random_prime_number(i)
    k = random.randint(1, p)
    if i < 24:
        start = time.time_ns()
        brutforce(k, p)
        end = time.time_ns()
        time1.append((end - start) / 1000000)

    start = time.time_ns()
    eyler(k, p)
    end = time.time_ns()

    time2.append((end - start) / 1000000)
    start = time.time_ns()
    euclidean_algorithms.PAE(k, p)
    end = time.time_ns()

    time3.append((end - start) / 1000000)

plt.subplot(211)
plt.plot(range(4, 24), time1, label="Brut force")
plt.legend()
plt.xticks(range(0, 24, 1))

plt.subplot(212)
plt.plot(range(4, interval), time2, label="Eyler")
plt.plot(range(4, interval), time3, label="PAE")
plt.xlabel('bit-length of i')
plt.ylabel('time spent (ms)')
plt.legend()
plt.show()
