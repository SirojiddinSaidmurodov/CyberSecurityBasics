import random

import RSA.Additional.quick_exp as exp


def is_prime_trial_division(n: int) -> bool:
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(pow(n, 0.5)), 2):
        if n % i == 0:
            return False
    return True


def is_prime_mr(n: int, rounds: int = 0) -> bool:
    if rounds == 0:
        rounds = n.bit_length()

    t = n - 1
    s = 0
    while True:
        if t % 2 == 0:
            t >>= 1
            s += 1
        else:
            break

    for i in range(rounds):
        a = random.randint(2, n - 1)
        x = exp.exp_mod(a, t, n)
        if x == 1 or x == n - 1:
            continue

        for j in range(s - 1):
            x = (x ** 2) % n
            if x == n - 1:
                break
        else:
            return False
    return True


if __name__ == "__main__":
    m = 4271
    print(is_prime_mr(m))
