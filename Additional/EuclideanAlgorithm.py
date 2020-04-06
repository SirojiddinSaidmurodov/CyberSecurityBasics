def euclidean(number1: int, number2: int):
    a = max(number1, number2)
    b = min(number1, number2)
    if b == 0:
        return a
    return euclidean(b, a % b)


print(euclidean(1071, 462))
