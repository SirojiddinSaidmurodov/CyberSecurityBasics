import math
import random

import RSA.Additional.euclidean_algorithms as euclid
import RSA.Additional.prime as prime
import RSA.Additional.quick_exp as exp


def get_random_prime_number(length: int) -> int:
    """
    Function returns random and prime number
    :param length bit length of result
    :type length: int
    """
    a = 2 ** (length - 1)
    b = (a * 2) - 1
    while True:
        result = random.randint(a, b)
        if prime.isPrimeMR(result, int(math.log(result, 2))):
            return result


def get_random_mutually_prime_number(number: int) -> int:
    """
    :return A random number that coprime (mutually prime) number
    :type number: int
    """
    while True:
        result = random.randint(1, number)
        if euclid.gcd(result, number) == 1:
            return result


def encrypt(m: int, key: tuple):
    e, n = key
    return exp.exp_mod(m, e, n)


class RSAKeyGen:
    def __init__(self, length: int = 512):
        self.isInit = False
        self.length = length
        self.fi = 0
        self.n = 0
        self.e = 0
        self.d = 0

    def get_public_key(self):
        if not self.isInit:
            p = get_random_prime_number(self.length)
            q = get_random_prime_number(self.length)
            self.fi = (p - 1) * (q - 1)
            self.n = p * q
            self.e = get_random_mutually_prime_number(self.fi)
            self.isInit = True
        return self.e, self.n

    def get_secret_key(self):
        if not self.isInit:
            raise Exception
        gcd, x, y = euclid.PAE(self.e, self.fi)
        while x < 0:
            x += self.fi
        while x > self.fi:
            x -= self.fi
        self.d = x
        return self.d

    def encrypt(self, m: int) -> int:
        if not self.isInit:
            raise Exception
        return exp.exp_mod(m, self.e, self.n)

    def decrypt(self, h: int) -> int:
        if not self.isInit:
            raise Exception
        return exp.exp_mod(h, self.d, self.n)

    def reset(self):
        self.isInit = False
        self.fi = 0
        self.n = 0
        self.e = 0
        self.d = 0


if __name__ == "__main__":
    print(RSAKeyGen().get_public_key())
