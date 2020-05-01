import math
import random

import RSA.Additional.EuclideanAlgorithm as euclide
import RSA.Additional.prime as prime


def get_random_prime(length: int) -> int:
    a = 2 ** (length - 1)
    b = (a * 2) - 1
    while True:
        result = random.randint(a, b)
        if prime.isPrimeMR(result, int(math.log(result, 2))):
            return result


def get_random_coprime(number: int) -> int:
    while True:
        result = random.randint(1, number)
        if euclide.euclidean(result, number) == 1:
            return result


class RSAKeyGen:
    def __init__(self):
        self.fi = 0
        self.n = 0
        self.e = 0

    def get_public_key(self, length: int):
        p = get_random_prime(length)
        q = get_random_prime(length)
        self.fi = (p - 1) * (q - 1)
        self.n = p * q
        self.e = get_random_coprime(self.fi)
        return self.e, self.n

    def get_decryption_key(self):
        if self.fi == 0:
            raise Exception
