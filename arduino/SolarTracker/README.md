# Solar Tracker Arduino

This version of the Solar Tracker uses only an Arduino with LDRs and a Stepper Motor to control the panels.

---

## How to run

---

1. Set up Solar Tracker values.

    The first tree lines of the sketch look like this:

    ``` c++
    #define ACCEPTABLE_DEVIATION 25
    #define STRATEGY_NAME "greedy"
    #define STEP_MODE "halfstep"
    ```

    Change the values in these three constants accordingly to your needs.

2. Connect the Stepper Motor accordingly to the diagram in the Diagram section and the LDRs in the ports A1 and A0 (left, right respectively).

3. Upload the sketch to the Arduino.

---

## Diagram

---

<img src="https://github.com/makersmovement-solartracking/solar-tracker-dkom/blob/master/diagrams/arduino-stepper-motor.png" alt="Connection between the Raspberry Pi and the Stepper Motor." width=500 height=500 />
