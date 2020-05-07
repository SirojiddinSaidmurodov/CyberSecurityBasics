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


interval = 100
time1 = []
time2 = []
time3 = []
for i in range(4, interval):
    print(i / interval * 100)
    p = get_random_prime_number(i)
    k = random.randint(1, p)
    if i < 25:
        start = time.time_ns()
        brutforce(k, p)
        end = time.time_ns()
        time1.append(abs(end - start))
    start = time.time_ns()
    eyler(k, p)
    end = time.time_ns()
    time2.append(abs(end - start))
    start = time.time_ns()
    euclidean_algorithms.PAE(k, p)
    end = time.time_ns()
    time3.append(abs(end - start))

plt.subplot(211)
plt.plot(range(4, 25), time1, label="Brut force")
plt.ticklabel_format(axis=1, style='%1.7f')
plt.ticklabel_format(axis=0, style='%2d')
plt.legend()

plt.subplot(212)
plt.plot(range(4, interval), time2, label="Eyler")
plt.plot(range(4, interval), time3, label="PAE")
plt.xlabel('bit-length of i')
plt.ylabel('time spent (ns)')
plt.ticklabel_format(axis=1, style='%1.7f')
plt.legend()
plt.show()
