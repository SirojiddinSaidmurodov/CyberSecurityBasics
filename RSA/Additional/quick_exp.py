def exp(a: int, b: int) -> int:
    result = 1
    e = bin(b)
    for i in range(b.bit_length()):
        if e[len(e) - 1 - i] == "1":
            result *= a
        a **= 2
    return result


def exp_mod(a: int, b: int, n: int) -> int:
    """
    Quick modular exponentiation of a to the bth power divided by n
    :return: reminder of <b>a</b> raised to the <b>b</b>th power divided by <b>n</b>
    :rtype: int
    :type a: int
    :type b: int
    :type n: int
    """
    result = 1
    e = bin(b)
    for i in range(b.bit_length()):
        if e[len(e) - 1 - i] == "1":
            result *= a
            result %= n
        a **= 2
        a %= n
    return result
