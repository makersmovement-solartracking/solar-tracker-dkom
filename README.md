# Solar Tracker DKOM

Solar Tracking Software using a Steper Motor.

---

### How to run the software

  1. Upload the I2C sketch into your Arduino.

  2. Pull the Docker image from Docker Hub or build it locally.
\
      **Building the Docker image:**

      ``` bash
      docker build -t solar-tracking-dkom .
      ```

      **Pulling from Docker Hub:**

      ``` bash
      docker pull sapmakers/solar-tracking-dkom
      ```

  3. Run the Docker container.
\
      **Image built locally:**

      ``` bash
      docker run --restart always --privileged --name stdkom -d -e EXEC_MODE=PROD -e ACCEPTABLE=DEVIATION={acceptable deviation} solar-tracking-dkom
      ```

      **Imaged pulled from Docker Hub:**

      ```bash
      docker run --restart always --privileged --name stdkom -d -e EXEC_MODE=PROD -e ACCEPTABLE_DEVIATION={acceptable_deviation} sapmakers/solar-tracking-dkom
      ```

      *Make sure to change the {acceptable_deviation} to an integer value.*  
      <br />

  4. Attach and logs:
    <br />
      * To attach to the container use the following command:

        ``` bash
        docker attach stdkom
        ```

      * To get the logs from the software use the following command:

        ``` bash
        docker logs stdkom
        ```

---

### Diagrams

#### Raspberry Pi and Stepper Motor Connection

![Connection between the Raspberry Pi and the Stepper Motor.][rasp-stepper]

[rasp-stepper]: https://github.com/makersmovement-solartracking/solar-tracker-dkom/diagrams/raspberry-and-stepper-motor.png "Raspberry and Stepper Motor Connection."

#### Raspberry Pi and Arduino I2C Connection

![I2C Connection between the Raspberry Pi and the Arduino.][rasp-arduino]

[rasp-arduino]: https://github.com/makersmovement-solartracking/solar-tracker-dkom/diagrams/raspberry-and-arduino.png "Raspberry and Arduino I2C connection."
