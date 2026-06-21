def ohms_law(
    voltage: float | None = None,
    current: float | None = None,
    resistance: float | None = None,
) -> dict[str, float]:
    given_values = [voltage is not None, current is not None, resistance is not None]

    if sum(given_values) != 2:
        raise ValueError("Enter exactly two values. Leave the unknown value empty.")

    if voltage is None:
        if current == 0:
            raise ValueError("Current cannot be zero when calculating voltage.")
        voltage = current * resistance

    elif current is None:
        if resistance == 0:
            raise ValueError("Resistance cannot be zero when calculating current.")
        current = voltage / resistance

    elif resistance is None:
        if current == 0:
            raise ValueError("Current cannot be zero when calculating resistance.")
        resistance = voltage / current

    return {
        "voltage": float(voltage),
        "current": float(current),
        "resistance": float(resistance),
    }
