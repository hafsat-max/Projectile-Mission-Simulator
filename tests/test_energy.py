from physics_lab.energy import kinetic_energy, potential_energy


def test_kinetic_energy():
    assert kinetic_energy(mass=2, velocity=3) == 9


def test_potential_energy():
    assert potential_energy(mass=2, gravity=9.81, height=10) == 196.2
