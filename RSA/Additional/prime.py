def isPrimeTrialDivision(n: int) -> bool:
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(pow(n, 0.5)), 2):
        if n % i == 0:
            return False
    return True
