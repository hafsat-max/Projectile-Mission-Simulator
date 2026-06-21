# Physics Lab Simulator

A beginner-friendly Python physics project with a command-line menu.

It can:

- Simulate projectile motion
- Plot and save a projectile graph
- Calculate Ohm's law
- Calculate pendulum period
- Calculate kinetic energy and gravitational potential energy

## 1. Setup

```bash
cd physics_lab_simulator
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2. Run the project

```bash
python main.py
```

## 3. Run tests

```bash
pytest
```

## Example

For projectile motion, try:

- Initial velocity: `30`
- Launch angle: `45`
- Gravity: `9.81`

The program will calculate time of flight, range, maximum height, and save a graph as:

```text
projectile_motion.png
```
