def euclidean(number1: int, number2: int):
    a = max(number1, number2)
    b = min(number1, number2)
    result = a % b
    if result == 0:
        return b
    return euclidean(b, result)


print(euclidean(1071, 462))
