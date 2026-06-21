MODULES = [
    {
        "number": "1",
        "name": "projectile",
        "title": "Projectile Motion",
        "description": "Simulate the path of a launched object",
        "handler": projectile_menu,
        "aliases": {"1", "projectile", "projectile motion", "motion"},
    },
    {
        "number": "2",
        "name": "ohms",
        "title": "Ohm's Law",
        "description": "Calculate voltage, current, or resistance",
        "handler": ohms_law_menu,
        "aliases": {"2", "ohms", "ohm", "ohms law", "electricity"},
    },
    {
        "number": "3",
        "name": "pendulum",
        "title": "Pendulum Period",
        "description": "Calculate the period of a simple pendulum",
        "handler": pendulum_menu,
        "aliases": {"3", "pendulum", "period"},
    },
    {
        "number": "4",
        "name": "energy",
        "title": "Energy Calculator",
        "description": "Calculate kinetic and potential energy",
        "handler": energy_menu,
        "aliases": {"4", "energy", "mechanical energy"},
    },
]


def show_dashboard() -> None:
    print("\nPhysics Lab Simulator")
    print("Explore a physics model below:\n")

    for module in MODULES:
        print(f"{module['number']}. {module['title']}")
        print(f"   {module['description']}")

    print("\nType a number, module name, or 'exit' to close the simulator.")


def find_module(user_input: str):
    user_input = user_input.strip().lower()

    for module in MODULES:
        if user_input in module["aliases"]:
            return module

    return None


def main() -> None:
    print("\nWelcome to Physics Lab Simulator")

    while True:
        show_dashboard()

        selected_option = input("\nWhat would you like to explore? ")

        if selected_option.strip().lower() in {"exit", "quit", "q"}:
            print("Session closed.")
            return

        selected_module = find_module(selected_option)

        if selected_module is None:
            print("\nThat module is not available. Try typing 'projectile', 'ohms', 'pendulum', or 'energy'.")
            continue

        print(f"\nOpening {selected_module['title']}...\n")
        selected_module["handler"]()