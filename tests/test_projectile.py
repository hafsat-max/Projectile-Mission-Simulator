import math

from physics_lab.projectile import simulate_projectile


def test_projectile_range_for_45_degrees():
    result = simulate_projectile(
        initial_velocity=30,
        angle_degrees=45,
        gravity=9.81,
    )

    expected_range = (30 ** 2) * math.sin(math.radians(90)) / 9.81

    assert result.range_distance == pytest_approx(expected_range, tolerance=0.01)


def pytest_approx(value, tolerance):
    return ApproxValue(value, tolerance)


class ApproxValue:
    def __init__(self, value, tolerance):
        self.value = value
        self.tolerance = tolerance

    def __eq__(self, other):
        return abs(other - self.value) <= self.tolerance
