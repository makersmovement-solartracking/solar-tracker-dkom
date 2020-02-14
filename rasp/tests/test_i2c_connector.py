import rasp.i2c_connector as i2c

def test_aggregate_bytes():
    """
    Assert aggregate_bytes is aggregating two bytes into a word correctly.
    """
    left = 0b10000000
    right = 0b00000001
    assert i2c.aggregate_bytes(left, right) == 32769


def test_empty_ldr_list():
    """
    Assert empty ldr_list is invalid.
    """
    ldr_list = []
    assert i2c.is_valid_ldr_list(ldr_list) is False


def test_odd_ldr_list():
    """
    Assert odd ldr_list is invalid.
    """
    ldr_list = [255, 255, 255]
    assert i2c.is_valid_ldr_list(ldr_list) is False


def test_even_ldr_list():
    """
    Assert even ldr_list is valid.
    """
    ldr_list = [255, 255, 255, 255]
    assert i2c.is_valid_ldr_list(ldr_list) is True


def test_invalid_ldr_values_list():
    """
    Assert ldr_list is validated as invalid when an even list with invalid
    values is passed.
    """
    ldr_list = [300, 487, 908, 65535]
    assert i2c.is_valid_ldr_data(ldr_list) is False


def test_valid_ldr_values_list():
    """
    Assert even ldr_list with valid values is validated as valid.
    """
    ldr_list = [300, 487, 908, 920]
    assert i2c.is_valid_ldr_data(ldr_list) is True
