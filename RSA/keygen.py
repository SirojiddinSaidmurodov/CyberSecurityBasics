import math
import random

import RSA.Additional.euclidean_algorithms as euclid
import RSA.Additional.prime as prime
import RSA.Additional.quick_exp as exp


def get_random_prime_number(length: int) -> int:
    a = 2 ** (length - 1)
    b = (a * 2) - 1
    while True:
        result = random.randint(a, b)
        if prime.isPrimeMR(result, int(math.log(result, 2))):
            return result


def get_random_mutually_prime_number(number: int) -> int:
    while True:
        result = random.randint(1, number)
        if euclid.gcd(result, number) == 1:
            return result


class RSAKeyGen:
    def __init__(self):
        self.isInit = False
        self.fi = 0
        self.n = 0
        self.e = 0
        self.d = 0

    def get_public_key(self, length: int):
        if not self.isInit:
            p = get_random_prime_number(length)
            q = get_random_prime_number(length)
            self.fi = (p - 1) * (q - 1)
            self.n = p * q
            self.e = get_random_mutually_prime_number(self.fi)
            self.isInit = True
        return self.e, self.n

    def get_decryption_key(self):
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
