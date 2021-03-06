from random import randint

import RSA.Additional.prime as prime
import RSA.Additional.quick_exp as exp
import RSA.rsa as rsa


def generate_public_keys_params(length):
    while True:
        q = rsa.get_random_prime_number(length - 1)
        p = 2 * q + 1
        if prime.is_prime_mr(p):
            break

    while True:
        g = randint(2, p - 2)
        if exp.exp_mod(g, 2, p) != 1 and exp.exp_mod(g, q, p) != 1:
            break

    a = randint(2, p - 2)
    return a, g, p


class DH:
    def __init__(self, length=128):
        self.g = 0
        self.p = 0
        self.secret_param = 0
        self.public_key = 0
        self.common_key = 0
        self.length = length

    def generate(self):
        self.secret_param, self.g, self.p = generate_public_keys_params(self.length)
        self.public_key = exp.exp_mod(self.g, self.secret_param, self.p)
        return self.g, self.p, self.public_key

    def calc_public_key(self, g, p):
        self.g = g
        self.p = p
        self.secret_param = randint(2, p - 2)
        self.public_key = exp.exp_mod(self.g, self.secret_param, self.p)
        return self.public_key

    def calc_common_key(self, peer_public_key):
        self.common_key = exp.exp_mod(peer_public_key, self.secret_param, self.p)
        return self.common_key


if __name__ == "__main__":
    Alice = DH()
    print()
    Bob = DH()
    x, y, z = Alice.generate()
    Bob.calc_public_key(Alice.g, Alice.p)
    print(x)
    print(x.bit_length())
    print(y)
    print(y.bit_length())
    print(z)
    print(z.bit_length())

    print(Alice.calc_common_key(Bob.public_key))
    print(Bob.calc_common_key(Alice.public_key))
