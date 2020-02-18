#define ACCEPTABLE_DEVIATION 25
#define STRATEGY_NAME "greedy"
#define STEP_MODE "halfstep"

// Stepper motor driver's pins
const int PINS[] = {8, 9, 10, 11};

// Pointer to a function that takes an array of integers as parameter
typedef String (*fptr)(int []);


// Strategies functions
String greedyMovement(int LDRValues[]) {
  /*
   * Given an array of LDR values, calculate the direction
   * with highest light incidence within an acceptable
   * deviation between the LDRs and returns the direction.
   */
    if(LDRValues[0] > LDRValues[1] + ACCEPTABLE_DEVIATION) {
        return "left";
    } else if(LDRValues[1] > LDRValues[0] + ACCEPTABLE_DEVIATION) {
        return "right";
    } else {
        return "stop";
    }
}

String noMovement(int LDRValues[]) {
  /*
   * Returns an stop string indicating no movement.
   */
    return "stop";
}

// Strategy list
fptr strategies(String strategy) {
  /*
   * Returns the Strategy function.
   * 
   * Each Strategy must have a if statement,
   * comparing the strategy passed as an argument
   * to the strategies created.
   */
      if(strategy.equalsIgnoreCase("greedy")) {
          return greedyMovement;
      } else {
          return noMovement;
      }
}

// Step Mode related functions

int (*(getStepMode)())[4] {
  /*
   * Returns the step mode matrix that contains
   * the activation sequence of the driver's pins.
   */
  if(STEP_MODE == "fullstep") {
    static int steps[8][4] = {
      {0, 0, 1, 1},
      {0, 1, 1, 0},
      {1, 1, 0, 0},
      {1, 0, 0, 1}
    };
    return steps;
  } else if(STEP_MODE == "wavestep") {
    static int steps[8][4] = {
      {0, 0, 0, 1},
      {0, 0, 1, 0},
      {0, 1, 0, 0},
      {1, 0, 0, 0}
    };
    return steps;
  } else if(STEP_MODE == "halfstep") {
    static int steps[8][4] = {
      {0, 0, 0, 1},
      {0, 0, 1, 1},
      {0, 0, 1, 0},
      {0, 1, 1, 0},
      {0, 1, 0, 0},
      {1, 1, 0, 0},
      {1, 0, 0, 0},
      {1, 0, 0, 1}
    };
    return steps;
  } else {
    static int steps[1][4] = {
      {0, 0, 0, 0}
    };
    return steps;
  }
}

int getStepsSize() {
  /*
   * Returns an integer indicating the size of the step mode matrix.
   */
  if(STEP_MODE == "halfstep") {
    return 8;
  } else if(STEP_MODE == "fullstep" || STEP_MODE == "wavestep") {
    return 4;
  } else {
    return 1;
  }
}

// Global Variables
fptr strategy;
int (*steps)[4];
bool nightModeActive;

void setup() {
    Serial.begin(9600);
    strategy = strategies(STRATEGY_NAME);

    steps = getStepMode();
    nightModeActive = false;

    for(int i=0; i < 4; i++) {
      pinMode(PINS[i], OUTPUT);
    }
}


void loop() {

  int LDRValues[] = {analogRead(A1), analogRead(A0)};

  nightMode(LDRValues);

  if(nightModeActive == false) {
    String direction = strategy(LDRValues);
  
    move(direction);
  
    delay(200);
  }
}

// Movement related function
void move(String direction) {
  /* 
   * Rotates the Stepper Motor accordingly to the direction passed.
   *   - If direction == right -> Clockwise.
   *   - If direction == left -> Counter-Clockwise.
   *   - If direction == stop -> Don't rotate.
   */

  int stepsSize = getStepsSize();
  
  if(direction == "right") {
    Serial.println("Rotating - Clockwise.");
    for(int i=0; i < stepsSize; i++) {
      for(int j=0; j < 4; j++) {
        digitalWrite(PINS[j], steps[i][j]);
      }
      delay(2);
    }
    return;
  }

  if(direction == "left") {
    Serial.println("Rotating - Counter-Clockwise.");
    for(int i=(stepsSize - 1); i >= 0; i--) {
      for(int j=0; j < 4; j++) {
        digitalWrite(PINS[j], steps[i][j]);
      }
      delay(2);
    }
    return;
  }

  if(direction == "stop") {
    Serial.println("Stopping.");
    for(int i = 0; i < 4; i++) {
      digitalWrite(PINS[i], 0);
    }
    return;
  }
}

void nightMode(int LDRValues[]) {
  if(LDRValues[0] < 10 && LDRValues[1] < 10) {
    move("stop");
    if(nightModeActive == false) {
      nightModeActive == true;
      Serial.println("Entering night mode.");
    }
    delay(300000);
  } else {
    if(nightModeActive == true) {
      Serial.println("Exiting night mode.");
      nightModeActive = false;
    }
  }
}
