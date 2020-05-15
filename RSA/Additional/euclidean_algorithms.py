def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def PAE(a, b):
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    while b != 0:
        q = a // b
        r = a % b
        a, b = b, r
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0
