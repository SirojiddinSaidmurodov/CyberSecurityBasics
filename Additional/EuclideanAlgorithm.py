def euclidean(a: int, b: int) -> int:
    while not b == 0:
        a, b = b, a % b
    return a


print(euclidean(1071, 462))
