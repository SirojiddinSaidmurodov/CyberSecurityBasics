def gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcd(b, a % b)
    return d, y, x - y * (a // b)


print(gcd(1071, 462))
