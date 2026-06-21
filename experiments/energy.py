def kinetic_energy(mass: float, velocity: float) -> float:
    if mass < 0:
        raise ValueError("Mass cannot be negative.")

    return 0.5 * mass * velocity ** 2


def potential_energy(mass: float, gravity: float, height: float) -> float:
    if mass < 0:
        raise ValueError("Mass cannot be negative.")
    if gravity < 0:
        raise ValueError("Gravity cannot be negative.")

    return mass * gravity * height
