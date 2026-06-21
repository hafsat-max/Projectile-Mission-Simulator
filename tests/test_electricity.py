from physics_lab.electricity import ohms_law


def test_ohms_law_current():
    result = ohms_law(voltage=12, resistance=4)

    assert result["current"] == 3


def test_ohms_law_voltage():
    result = ohms_law(current=2, resistance=5)

    assert result["voltage"] == 10
