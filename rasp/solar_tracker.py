import logging
import logging.config

import signal

from time import sleep

from controller import GPIO, Driver, InvalidMovementException
from i2c_connector import (I2C, InvalidLDRListException,
                                InvalidLDRListValuesException)

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class SolarTracker:

    """
    Class that represents the Solar Tracker application with all the
    components, motor and i2c controllers. 

    Attributes:
        address {int} -- Address of the I2C slave device.
        acceptable_deviation {int} -- Acceptable deviation between two LDRs
        output_pins {list} -- List with the GPIO output pins
        ldr_count {int} -- Number of Light Dependent Resistors (default: {"2"})

    Methods:
        _no_movement()
            Empty strategy which will not move the panels

        _greedy_movement(ldr_values)
            Returns the direction with the highest amount of light

        night_time_mode(ldr_values)
            Verifies if the light is low enough to activate night mode

        run(strategy)
            Executes the tracking process, requesting the LDR data from the
            I2C Slave device, comparing accordingly to the strategy, and
            rotating the solar panels.
    """

    def __init__(self, address, acceptable_deviation,
                 output_pins, step_mode, ldr_count=2):

        self.acceptable_deviation = acceptable_deviation

        self.controller = Driver(output_pins, step_mode)
        self.i2c = I2C(address, ldr_count)

        self.strategies = {
            "empty": self._no_movement,
            "greedy": self._greedy_movement,
        }

        signal.signal(signal.SIGINT, GPIO.cleanup)
        signal.signal(signal.SIGTERM, GPIO.cleanup)

        self.night_mode = False

    def _no_movement(self, ldr_values):
        """
        Strategy that contains no movement.
        
        Arguments:
            ldr_values {list} -- List with the LDR values.
        
        Returns:
            [str] -- Movement to be executed by the motor.
        """
        return "stop"

    def _greedy_movement(self, ldr_values):
        """
        Strategy that compares the LDR values and return the direction
        with the highest amount of light.
        
        Arguments:
            ldr_values {list} -- List with the LDR values.
        
        Returns:
            [str] -- Movement to be executed by the motor.
        """
        if ldr_values[0] > ldr_values[1] + self.acceptable_deviation:
            return "left"
        if ldr_values[1] > ldr_values[0] + self.acceptable_deviation:
            return "right"
        return "stop"

    def night_time_mode(self, ldr_values):
        """
        Stops the execution of the process during some time before requesting
        a new set of values due to the small amount of light.

        Arguments:
            ldr_values {list} -- List with the LDR values.
        """

        if ldr_values[0] < 10 and ldr_values[1] < 10:
            self.controller.move("stop")
            if self.night_mode is False:
                logger.info("Entering night mode...")
                self.night_mode = True
            sleep(300)
        elif self.night_mode:
            logger.info("Exiting night mode!")
            self.night_mode = False

    def run(self, strategy="empty"):
        """
        Execute the tracking process, request new LDR values five times 
	per second, validates them, compares them accordingly to the
	strategy and execute the movement.
        
        Keyword Arguments:
            strategy {str} -- Strategy used by the tracking system.
                              (default: {"empty"})
        
        Raises:
            Exception: Strategy not created.
        """
        if strategy not in self.strategies.keys():
            raise Exception("Invalid strategy!")
        while True:
            try:
                sleep(0.2)
                ldr_values = self.i2c.get_ldr_values()

            except (IOError, OSError) as e:
                logger.exception(str(e))
                continue

            except (InvalidLDRListException, InvalidLDRListValuesException) as e:
                self.controller.move("stop")
                logger.exception(str(e))
                continue

            self.night_time_mode(ldr_values)

            movement = self.strategies[strategy](ldr_values)
            
            try:
                self.controller.move(movement)
            except InvalidMovementException as e:
                logger.exception(str(e))
