import math


def pendulum_period(length: float, gravity: float = 9.81) -> float:
    if length <= 0:
        raise ValueError("Length must be greater than 0.")
    if gravity <= 0:
        raise ValueError("Gravity must be greater than 0.")

    return 2 * math.pi * math.sqrt(length / gravity)
