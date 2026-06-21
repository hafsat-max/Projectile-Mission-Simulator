import math
from dataclasses import dataclass

import matplotlib.pyplot as plt


@dataclass
class ProjectileResult:
    time_values: list[float]
    x_values: list[float]
    y_values: list[float]
    time_of_flight: float
    max_height: float
    range_distance: float


def simulate_projectile(
    initial_velocity: float,
    angle_degrees: float,
    gravity: float = 9.81,
    time_step: float = 0.02,
) -> ProjectileResult:
    if initial_velocity <= 0:
        raise ValueError("Initial velocity must be greater than 0.")
    if gravity <= 0:
        raise ValueError("Gravity must be greater than 0.")
    if time_step <= 0:
        raise ValueError("Time step must be greater than 0.")

    angle_radians = math.radians(angle_degrees)

    velocity_x = initial_velocity * math.cos(angle_radians)
    velocity_y = initial_velocity * math.sin(angle_radians)

    time_of_flight = (2 * velocity_y) / gravity
    max_height = (velocity_y ** 2) / (2 * gravity)
    range_distance = velocity_x * time_of_flight

    time_values = []
    x_values = []
    y_values = []

    time = 0.0

    while time <= time_of_flight:
        x = velocity_x * time
        y = velocity_y * time - 0.5 * gravity * time ** 2

        if y >= 0:
            time_values.append(time)
            x_values.append(x)
            y_values.append(y)

        time += time_step

    return ProjectileResult(
        time_values=time_values,
        x_values=x_values,
        y_values=y_values,
        time_of_flight=time_of_flight,
        max_height=max_height,
        range_distance=range_distance,
    )


def plot_projectile(result: ProjectileResult, filename: str = "projectile_motion.png") -> None:
    plt.figure()
    plt.plot(result.x_values, result.y_values)
    plt.title("Projectile Motion")
    plt.xlabel("Horizontal Distance, x (m)")
    plt.ylabel("Vertical Height, y (m)")
    plt.grid(True)
    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close()
