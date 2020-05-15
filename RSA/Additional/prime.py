import random

import RSA.Additional.quick_exp as exp


def isPrimeTrialDivision(n: int) -> bool:
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(pow(n, 0.5)), 2):
        if n % i == 0:
            return False
    return True


def isPrimeMR(n: int, rounds: int) -> bool:
    found = False
    t = n - 1
    s = 0
    while not found:
        if t % 2 == 0:
            t >>= 1
            s += 1
        else:
            found = True

    for i in range(rounds):
        a = random.randint(2, n - 1)
        x = exp.exp_mod(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(s - 1):
            x = (x ** 2) % n
            if x == n - 1:
                break
        return False
    return True


if __name__ == "__main__":
    print(isPrimeMR(53, (50).bit_length()))
