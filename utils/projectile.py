import math


def calculate_projectile_motion(
    initial_velocity: float,
    launch_angle_degrees: float,
    gravity: float,
    time_step: float = 0.02,
) -> dict:
    # Resolve initial velocity into components:
    # u_x = u cos(theta), u_y = u sin(theta)
    angle_radians = math.radians(launch_angle_degrees)
    velocity_x = initial_velocity * math.cos(angle_radians)
    velocity_y = initial_velocity * math.sin(angle_radians)

    # Time of flight for same launch and landing height:
    # T = 2u_y / g
    time_of_flight = (2 * velocity_y) / gravity

    # Maximum height:
    # H = u_y² / 2g
    max_height = (velocity_y ** 2) / (2 * gravity)

    # Horizontal range:
    # R = u_x T
    range_distance = velocity_x * time_of_flight

    time_values = []
    x_values = []
    y_values = []

    time = 0.0

    while time <= time_of_flight:
        # Horizontal position: x = u_x t
        x = velocity_x * time

        # Vertical position: y = u_y t - 1/2 gt²
        y = velocity_y * time - 0.5 * gravity * time ** 2

        if y >= 0:
            time_values.append(time)
            x_values.append(x)
            y_values.append(y)

        time += time_step

    return {
        "time": time_values,
        "x": x_values,
        "y": y_values,
        "velocity_x": velocity_x,
        "velocity_y": velocity_y,
        "time_of_flight": time_of_flight,
        "max_height": max_height,
        "range": range_distance,
    }


def suggest_angles_for_target(
    initial_velocity: float,
    target_distance: float,
    gravity: float,
) -> tuple[float, float] | None:
    # From range equation:
    # R = u² sin(2theta) / g
    # sin(2theta) = gR / u²
    value = (gravity * target_distance) / (initial_velocity ** 2)

    if value > 1:
        return None

    low_angle = 0.5 * math.degrees(math.asin(value))
    high_angle = 90 - low_angle

    return low_angle, high_angle


def describe_landing(
    range_distance: float,
    target_distance: float,
    hit_tolerance: float,
) -> str:
    difference = range_distance - target_distance

    if abs(difference) <= hit_tolerance:
        return "Hit"

    if difference < 0:
        return "Lands short"

    return "Overshoots"