import pytest

from rasp.controller import (Driver, InvalidMovementException,
                             InvalidStepModeException)


def test_invalid_step_type_should_raise_exception():
    """
    Assert passing invalid step type to Driver raises InvalidStepException.
    """

    with pytest.raises(InvalidStepModeException) as excinfo:
        Driver([21, 22], "invalid")

    assert "Invalid Step Mode" in str(excinfo.value)


def test_invalid_movement_shoudl_raise_exception():
    """
    Assert using invalid movement in the move() method raises
    InvalidMovementException.
    """
    
    with pytest.raises(InvalidMovementException) as excinfo:
        driver = Driver([21, 22], "halfstep")
        driver.move("invalid")

    assert "Invalid Movement" in str(excinfo.value)