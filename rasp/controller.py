import logging
import logging.config

import time

from enum import Enum

import gpio_connector as GPIO

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Driver:
    """
    Class that represents a Stepper Driver, which controls the behavior
    of the Stepper Motor.
    """

    def __init__(self, output_pins, step_mode):

        self.movements = {
            "stop": Movement.stop,
            "right": Movement.right,
            "left": Movement.left
        }

        self.steps = {
            "halfstep": StepperMode.HALFSTEP,
        }

        self.output_pins = output_pins

        self.set_step_mode(step_mode)

        GPIO.setmode(GPIO.BCM)

        self.initialize_output_pins()

        GPIO.setwarnings(False)

    def set_step_mode(self, step_mode):
        """

        Set self.step_mode to the given step_mode if it is a valid type.
        
        Arguments:
            step_mode {string} -- String naming the step type
        
        Raises:
            InvalidStepModeException: Step type not defined in the Steps enum
        """

        if step_mode not in self.steps:
            raise InvalidStepModeException
        else:
            self.step_mode = step_mode

    def move(self, direction):
        """
        Rotates the solar modules axis to a given direction.

        
        Arguments:
            direction {string} -- String naming the direction the axis should
                                  rotate
        
        Raises:
            InvalidMovementException: Movement not defined in the Movement enum
        """

        if direction not in self.movements.keys():
            raise InvalidMovementException
        else:
            self.movements[direction](self.output_pins,
                                      self.steps[self.step_mode].value)

    def initialize_output_pins(self):
        """
        Initializes the pins as output and set the energy to low.
        """
        for pin in self.output_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)


class Movement(Enum):
    """
    Enumerator with the movements executed by the Stepper motor.
    """

    @classmethod
    def stop(cls, output_pins, steps):
        """
        Stops the panel axis' movements
        
        Arguments:
            output_pins {list} -- List with the output pins
        """

        for pin in output_pins:
            GPIO.output(pin, GPIO.LOW)

        logger.info("Stopped the movements")

    @classmethod
    def left(cls, output_pins, steps):
        """ 
        Rotates the panels anti-clockwise.
        
        Arguments:
            output_pins {list} -- List of output pins
            steps {list} -- 2D list of the steps
        """

        for halfstep in range(len(steps)):

            for pin in range(len(output_pins)):
        
                GPIO.output(output_pins[pin], steps[halfstep][pin])

            time.sleep(0.001)

        logger.info("Turning the panels to the left")

    @classmethod
    def right(cls, output_pins, steps):
        """
        Rotate the panels clockwise

        Arguments:
            output_pins {list} -- List of output pins
            steps {list} -- 2D list of the steps
        """

        for halfstep in reversed(range(len(steps))):

            for pin in range(len(output_pins)):
        
                GPIO.output(output_pins[pin], steps[halfstep][pin])

            time.sleep(0.001)

        logger.info("Turning the panels to the right")


class StepperMode(Enum):
    """
    Enumerator containg the modes for the steppers motor.
    """
    HALFSTEP = [[1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1]]


class InvalidMovementException(Exception):

    def __str__(self):
        return "InvalidMovementException: Invalid Movement."


class InvalidStepModeException(Exception):

    def __str__(self):
        return "InvalidStepModeException: Invalid Step Mode."
