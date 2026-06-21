import math

import matplotlib.pyplot as plt
import streamlit as st


GRAVITY_PRESETS = {
    "Earth": 9.81,
    "Moon": 1.62,
    "Mars": 3.71,
    "Jupiter": 24.79,
}

PLANET_COLORS = {
    "Earth": "#22c55e",
    "Moon": "#cbd5e1",
    "Mars": "#f97316",
    "Jupiter": "#f59e0b",
}

STATUS_COLORS = {
    "Hit": "#22c55e",
    "Lands short": "#f97316",
    "Overshoots": "#ef4444",
}


def calculate_projectile_motion(
    initial_velocity: float,
    launch_angle_degrees: float,
    gravity: float,
    time_step: float = 0.02,
) -> dict:
    # Resolve initial velocity into horizontal and vertical components:
    # u_x = u cos(theta), u_y = u sin(theta)
    angle_radians = math.radians(launch_angle_degrees)
    velocity_x = initial_velocity * math.cos(angle_radians)
    velocity_y = initial_velocity * math.sin(angle_radians)

    # Time of flight for a projectile landing at the same height:
    # T = 2u_y / g
    time_of_flight = (2 * velocity_y) / gravity

    # Maximum height reached by the projectile:
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
        # Horizontal position:
        # x = u_x t
        x = velocity_x * time

        # Vertical position:
        # y = u_y t - 1/2 gt²
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
    # Range formula for same launch and landing height:
    # R = u² sin(2theta) / g
    #
    # Rearranged:
    # sin(2theta) = gR / u²
    value = (gravity * target_distance) / (initial_velocity ** 2)

    if value > 1:
        return None

    # First possible angle:
    # theta_1 = 1/2 sin⁻¹(gR / u²)
    low_angle = 0.5 * math.degrees(math.asin(value))

    # Second possible angle:
    # theta_2 = 90° - theta_1
    high_angle = 90 - low_angle

    return low_angle, high_angle


def describe_landing(range_distance: float, target_distance: float, hit_tolerance: float) -> str:
    difference = range_distance - target_distance

    if abs(difference) <= hit_tolerance:
        return "Hit"
    if difference < 0:
        return "Lands short"
    return "Overshoots"


def metric_card(title: str, value: str, color: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 5px solid {color};">
            <p class="metric-title">{title}</p>
            <h3 style="color: {color};">{value}</h3>
            <p class="metric-note">{note}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Projectile Mission Simulator",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(139, 92, 246, 0.22), transparent 32%),
                radial-gradient(circle at bottom left, rgba(56, 189, 248, 0.16), transparent 35%),
                linear-gradient(135deg, #050816 0%, #0b1026 50%, #111827 100%);
            color: #f8fafc;
        }

        .block-container {
            padding-top: 2rem;
            max-width: 1280px;
        }

        h1 {
            font-size: 3.2rem !important;
            font-weight: 800 !important;
            background: linear-gradient(90deg, #f8fafc, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        h2, h3 {
            color: #f8fafc !important;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 1.05rem;
            max-width: 780px;
            line-height: 1.7;
        }

        .pill {
            display: inline-block;
            padding: 0.45rem 0.85rem;
            border-radius: 999px;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: #38bdf8;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .section-card {
            padding: 1.2rem;
            border-radius: 22px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.28);
        }

        .metric-card {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 16px 28px rgba(0, 0, 0, 0.24);
            min-height: 120px;
        }

        .metric-title {
            color: #94a3b8;
            font-size: 0.85rem;
            margin-bottom: 0.35rem;
            font-weight: 600;
        }

        .metric-card h3 {
            font-size: 1.75rem;
            margin: 0;
        }

        .metric-note {
            color: #cbd5e1;
            font-size: 0.8rem;
            margin-top: 0.35rem;
        }

        .formula-box {
            padding: 0.85rem 1rem;
            border-radius: 16px;
            background: rgba(2, 6, 23, 0.72);
            border: 1px solid rgba(56, 189, 248, 0.2);
            margin-bottom: 0.6rem;
        }

        div[data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
        }

        .stSlider label, .stSelectbox label {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="select"] > div {
            background-color: rgba(15, 23, 42, 0.95);
            border-color: rgba(148, 163, 184, 0.25);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Projectile Mission Simulator")

st.markdown(
    """
    <p class="hero-subtitle">
        Launch a projectile across different worlds and see how speed, angle, and gravity decide
        whether it reaches the target.
    </p>

    <span class="pill">Python</span>
    <span class="pill">Streamlit</span>
    <span class="pill">Projectile motion</span>
    <span class="pill">No air resistance model</span>
    """,
    unsafe_allow_html=True,
)

st.divider()

def formula_line(title: str, formula: str, color: str = "#38bdf8") -> None:
    st.markdown(
        f"""
        <p style="margin-bottom: 0.8rem;">
            <strong>{title}:</strong>
            <span style="color: {color}; font-weight: 700;">{formula}</span>
        </p>
        """,
        unsafe_allow_html=True,
    )
    
with st.expander("Physics model used in this simulator"):
    st.write(
        "This model assumes no air resistance and assumes the projectile lands at the same height from which it was launched."
    )

    col1, col2 = st.columns(2)
    
    with col1:
        formula_line("Horizontal velocity", "uₓ = u cos(θ)")

    with col2:
        formula_line("Vertical velocity", "uᵧ = u sin(θ)")

    col3, col4 = st.columns(2)

    with col3:
        formula_line("Horizontal position", "x = uₓt")

    with col4:
        formula_line("Vertical position", "y = uᵧt − ½gt²")

    col5, col6 = st.columns(2)

    with col5:
        formula_line("Time of flight", "T = 2uᵧ / g")

    with col6:
        formula_line("Maximum height", "H = uᵧ² / 2g")

    col7, col8 = st.columns(2)

    with col7:
        formula_line("Horizontal range", "R = u²sin(2θ) / g")

    with col8:
        formula_line("Target angle relation", "sin(2θ) = gR / u²")
        
left_column, right_column = st.columns([1, 2], gap="large")

with left_column:

    st.subheader("Mission Controls")

    selected_planet = st.selectbox(
        "Gravity environment",
        list(GRAVITY_PRESETS.keys()),
        index=2,
    )

    gravity = GRAVITY_PRESETS[selected_planet]
    planet_color = PLANET_COLORS[selected_planet]

    initial_velocity = st.slider(
        "Launch speed, u (m/s)",
        min_value=5,
        max_value=200,
        value=50,
    )

    launch_angle = st.slider(
        "Launch angle, θ (degrees)",
        min_value=1,
        max_value=89,
        value=45,
    )

    target_distance = st.slider(
        "Target distance (m)",
        min_value=10,
        max_value=2000,
        value=250,
    )

    hit_tolerance = st.slider(
        "Hit tolerance (m)",
        min_value=1,
        max_value=50,
        value=10,
    )

    st.markdown(
        f"""
        <div class="formula-box" style="border-color: {planet_color};">
            <strong style="color: {planet_color};">Gravity on {selected_planet}</strong><br>
            <span style="color: #cbd5e1;">g = {gravity} m/s²</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


result = calculate_projectile_motion(
    initial_velocity=initial_velocity,
    launch_angle_degrees=launch_angle,
    gravity=gravity,
)

landing_status = describe_landing(
    range_distance=result["range"],
    target_distance=target_distance,
    hit_tolerance=hit_tolerance,
)

status_color = STATUS_COLORS[landing_status]

suggested_angles = suggest_angles_for_target(
    initial_velocity=initial_velocity,
    target_distance=target_distance,
    gravity=gravity,
)

with right_column:
    st.subheader("Trajectory")

    fig, ax = plt.subplots(figsize=(10, 5))

    fig.patch.set_facecolor("#0b1026")
    ax.set_facecolor("#020617")

    ax.plot(
        result["x"],
        result["y"],
        linewidth=3,
        color="#38bdf8",
        label="Projectile path",
    )

    ax.axvline(
        target_distance,
        linestyle="--",
        linewidth=2,
        color="#8b5cf6",
        label="Target position",
    )

    ax.scatter(
        [target_distance],
        [0],
        s=110,
        color="#8b5cf6",
        label="Target",
        zorder=5,
    )

    ax.scatter(
        [result["range"]],
        [0],
        s=110,
        color=status_color,
        label="Landing point",
        zorder=5,
    )

    ax.set_title(
        f"Launch on {selected_planet}",
        color="#f8fafc",
        fontsize=16,
        fontweight="bold",
    )

    ax.set_xlabel("Horizontal distance, x (m)", color="#cbd5e1")
    ax.set_ylabel("Vertical height, y (m)", color="#cbd5e1")

    ax.grid(True, color="#334155", alpha=0.65)

    ax.tick_params(colors="#cbd5e1")

    for spine in ax.spines.values():
        spine.set_color("#475569")

    legend = ax.legend()
    legend.get_frame().set_facecolor("#0f172a")
    legend.get_frame().set_edgecolor("#334155")

    for text in legend.get_texts():
        text.set_color("#f8fafc")

    st.pyplot(fig)


st.divider()

st.subheader("Mission Result")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    metric_card(
        "Landing Status",
        landing_status,
        status_color,
        "Based on the selected target distance",
    )

with metric_col2:
    metric_card(
        "Range",
        f"{result['range']:.2f} m",
        "#38bdf8",
        "Horizontal distance travelled",
    )

with metric_col3:
    metric_card(
        "Maximum Height",
        f"{result['max_height']:.2f} m",
        "#8b5cf6",
        "Highest point reached",
    )

with metric_col4:
    metric_card(
        "Time of Flight",
        f"{result['time_of_flight']:.2f} s",
        "#22c55e",
        "Total time in the air",
    )

st.divider()

st.subheader("Velocity Components")

component_col1, component_col2 = st.columns(2)

with component_col1:
    metric_card(
        "Horizontal velocity",
        f"{result['velocity_x']:.2f} m/s",
        "#38bdf8",
        "uₓ = u cosθ",
    )

with component_col2:
    metric_card(
        "Vertical velocity",
        f"{result['velocity_y']:.2f} m/s",
        "#8b5cf6",
        "uᵧ = u sinθ",
    )

st.divider()

st.subheader("Target Angle Suggestion")

if suggested_angles is None:
    st.markdown(
        """
        <div class="formula-box" style="border-color: #f97316;">
            <strong style="color: #f97316;">Target is too far away</strong><br>
            <span style="color: #cbd5e1;">
                With this launch speed and gravity, the projectile cannot reach the selected target.
                Increase the launch speed or choose a lower-gravity planet.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    low_angle, high_angle = suggested_angles

    st.write(
        f"To reach a target at **{target_distance} m**, the same launch speed can use two possible angles:"
    )

    angle_col1, angle_col2 = st.columns(2)

    with angle_col1:
        metric_card(
            "Low-angle shot",
            f"{low_angle:.2f}°",
            "#38bdf8",
            "Flatter and faster path",
        )

    with angle_col2:
        metric_card(
            "High-angle shot",
            f"{high_angle:.2f}°",
            "#8b5cf6",
            "Higher and longer path",
        )