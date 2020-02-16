import quick2wire.i2c as i2c

class I2C:
    """
    Class that represents the communication between the Arduino and the
    Raspberry Pi.
    """

    def __init__(self, address, number_of_ldrs=2):
        self.SLAVE_ADDRESS = address
        self.number_of_ldrs = number_of_ldrs

    def get_arduino_data(self):
        """
        Get the data transfered through the I2C from the Arduino
        
        Returns:
            list -- List with n bytes representing the LDR values.
        """

        with i2c.I2CMaster() as bus:
            data = bus.transaction(i2c.reading(self.SLAVE_ADDRESS,
                                               self.number_of_ldrs * 2))
            ldr_values = [data[0][i] for i in range(self.number_of_ldrs *2)]
            
            return ldr_values

    def get_ldr_values(self):
        """

        Get the LDR values and validates them.
        
        Raises:
            InvalidLDRListException: LDR list is odd or empty
            InvalidLDRListValuesException: LDR list has invalid values
        
        Returns:
            list -- List with the LDR values.
        """
        brute_data = self.get_arduino_data()
        ldr_values = convert_byte_to_integer(brute_data)
        if not is_valid_ldr_list(ldr_values):
            raise InvalidLDRListException
        if not is_valid_ldr_data(ldr_values):
            raise InvalidLDRListValuesException
        return ldr_values


def convert_byte_to_integer(data):
    """
    Convert the byte data to an integer. 

    Arguments:
        data {int} -- Byte that represents an integer.
    
    Returns:
        list -- List with the LDR values.
    """
    ldr_data = []
    for i in range(int(len(data)/2)):
        ldr_data.append(aggregate_bytes(data[i*2], data[i*2 + 1]))
    
    return ldr_data


def aggregate_bytes(most_representative, least_representative):
    """
    Aggregates n bytes into a single word.

    Arguments:
        most_representative {int} -- Most representative bytes
        least_representative {int} -- Least representative bytes
    
    Returns:
        int -- Byte that represents an integer.
    """
    return (most_representative << 8 | least_representative) & 0xffffffff


def is_valid_ldr_list(ldr_list):
    """
    Validates the LDR list, verifying its size.
    
    Arguments:
        ldr_list {list} -- List containing the LDR values.
    
    Returns:
        bool -- Boolean representing the validity of the LDR list
    """
    if not ldr_list or len(ldr_list) % 2 != 0:
        return False
    else:
        return True


def is_valid_ldr_data(ldr_list):
    """
    Validates the LDR values, verifying if they're in the range 0 - 1023
    
    Arguments:
        ldr_list {list} -- List containing the LDR values.
    
    Returns:
        bool -- Boolean representing the validity of the LDR values
    """
    if 65535 in ldr_list:
        return False
    else:
        return True


class InvalidLDRListException(Exception):
    """
    Exception for an invalid LDR list.
    """

    def __init__(self):
        self.msg = "Invalid LDR List. The transfered list "\
                   "is either odd or empty."

    def __str__(self):
        return repr(self.msg)


class InvalidLDRListValuesException(Exception):
    """
    Exception for an invalid ldr list.
    """

    def __init__(self):
        self.msg = "Invalid LDR Value. The LDR values will not be used."

    def __str__(self):
        return repr(self.msg)
