from random import randint

import RSA.Additional.prime as prime
import RSA.Additional.quick_exp as exp
import RSA.rsa as rsa


def generate_public_keys_params(length=128):
    while True:
        q = rsa.get_random_prime_number(length)
        p = 2 * q + 1
        if prime.is_prime_mr(p):
            break

    g = randint(2, p)
    a = randint(2, p)
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
        self.secret_param = randint(2, p)
        return exp.exp_mod(self.g, self.secret_param, self.p)

    def calc_common_key(self, peer_public_key):
        self.common_key = exp.exp_mod(peer_public_key, self.secret_param, self.p)
        return self.common_key


if __name__ == "__main__":
    print(generate_public_keys_params())
