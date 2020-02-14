from solar_tracker import SolarTracker

if __name__ == "__main__":
    ARDUINO_ADDRESS = 0X08
    ACCEPTABLE_DEVIATION = 50
    OUTPUT_PINS = [21,20,16,12]
    STEP_MODE = "halfstep"
    LDR_COUNT = 2

    solar_tracker = SolarTracker(address=ARDUINO_ADDRESS,
                                 acceptable_deviation=ACCEPTABLE_DEVIATION,
                                 output_pins=OUTPUT_PINS,
                                 step_mode=STEP_MODE,
                                 ldr_count=LDR_COUNT)

    solar_tracker.run(strategy="greedy")
