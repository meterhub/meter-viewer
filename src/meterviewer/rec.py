from . import types as T


def is_carry_over(digit: T.DigitInt):
    if digit[-1] == 0 or digit[-1] == 9:
        return True
    return False
