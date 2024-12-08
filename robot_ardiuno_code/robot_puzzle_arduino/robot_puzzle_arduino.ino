const int motor1Pin1 = 22;  // Motor 1 control pin 1
const int motor1Pin2 = 23;  // Motor 1 control pin 2
const int motor2Pin1 = 24;  // Motor 2 control pin 1
const int motor2Pin2 = 25;  // Motor 2 control pin 2
const int motor3Pin1 = 26;  // Motor 3 control pin 1
const int motor3Pin2 = 27;  // Motor 3 control pin 2
const int motor4Pin1 = 28;  // Motor 4 control pin 1
const int motor4Pin2 = 29;  // Motor 4 control pin 2
const int motor5Pin1 = 31;  // Motor 5 control pin 1
const int motor5Pin2 = 30;  // Motor 5 control pin 2
const int positionPin1 = A0; // Analog pin for Motor 1 position reading
const int positionPin2 = A1; // Analog pin for Motor 2 position reading
const int positionPin3 = A2; // Analog pin for Motor 3 position reading
const int positionPin4 = A14; 
const int positionPin5 = A15; // Analog pin for Motor 5 position reading

// Motor position limits and mappings
const int motor1Min = 290, motor1Max = 510, mapped1Min = 0, mapped1Max = 90;
const int motor2Min = 150, motor2Max = 950, mapped2Min = -45, mapped2Max = 45;
const int motor3Min = 140, motor3Max = 460, mapped3Min = 0, mapped3Max = 90;
const int motor4Min = 340, motor4Max = 930, mapped4Min = -90, mapped4Max = 90;
const int motor5Min = 520, motor5Max = 860, mapped5Min = 0, mapped5Max = -90;

#include "Stepper.h"

// Define number of steps per rotation:
const int stepsPerRevolution = 2048;
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);


// Setup function
void setup() {
  Serial.begin(9600); // Start serial communication
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(motor3Pin1, OUTPUT);
  pinMode(motor3Pin2, OUTPUT);
  pinMode(motor4Pin1, OUTPUT);
  pinMode(motor4Pin2, OUTPUT);
  pinMode(motor5Pin1, OUTPUT);
  pinMode(motor5Pin2, OUTPUT);
  myStepper.setSpeed(5);
}

// Loop function
void loop() {
  //printMotorPositions();
  if (Serial.available()) {
   
    String command = Serial.readStringUntil('\n'); // Read command until newline
    //Serial.println(command);
    if (command == "R90") {
      myStepper.step(stepsPerRevolution/4);
    }

    else if (command == "R180") {
      myStepper.step(stepsPerRevolution/2);
    }

     else if (command == "R270") {
      myStepper.step(3*stepsPerRevolution/4);
    }

    else {
      if (command =="0"){

        command="m5to0;m2to51;m3to-62;m4to10;m1to-15;";
      }
      else if (command =="1"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to0;m1to45;m3to15;m4to20;m2to-55;m5to0;";
      }
      else if (command =="2"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to0;m1to30;m2to0;m3to15;m4to20;m2to-55;m5to0;";
      }
      else if (command =="3"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to0;m1to15;m2to0;m3to15;m4to20;m2to-55;m5to0;";
      }

      else if (command =="4"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to0;m1to55;m4to30;m3to-40;m2to-15;m5to0;";
      }

      else if (command =="5"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to0;m1to40;m4to30;m3to-40;m2to-15;m5to0;";
      }

      else if (command =="6"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to0;m1to25;m4to30;m3to-40;m2to-15;m5to0;";
      }
      
      else if (command =="7"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to20;m1to50;m4to35;m3to-57;m2to0;m5to0;";
      }
      
      else if (command =="8"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to0;m1to45;m4to35;m3to-57;m5to0;";
      }

      else if (command =="9"){
        myStepper.step(stepsPerRevolution/4);
        delay(1000);
        command="m4to-10;m5to70;m3to0;m2to0;m1to30;m4to35;m3to-57;m5to0;";
      }
      
      // Process other commands
      int startIndex = 0;
      int commaIndex = command.indexOf(';');

      while (commaIndex >= 0) {
        String singleCommand = command.substring(startIndex, commaIndex);
        processCommand(singleCommand);
        startIndex = commaIndex + 1;
        commaIndex = command.indexOf(';', startIndex);
      }

      // Process the last command
      String lastCommand = command.substring(startIndex);
      processCommand(lastCommand);
    }
  }

//  // Read motor positions
//  analogRead(positionPin1);
//  analogRead(positionPin2);
//  analogRead(positionPin3);
//  analogRead(positionPin4);
//  analogRead(positionPin5);
}

// Process individual commands
void processCommand(String command) {
  if (command.startsWith("m1to")) {
    int targetAngle = command.substring(4).toInt();
    int targetPosition = map(targetAngle, mapped4Min, mapped4Max, motor4Min, motor4Max);
    moveToPosition(motor4Pin1, motor4Pin2, positionPin4, targetPosition);
  } 
  else if (command.startsWith("m2to")) {
    int targetAngle = command.substring(4).toInt();
    int targetPosition = map(targetAngle, mapped5Min, mapped5Max, motor5Min, motor5Max);
    moveToPosition(motor5Pin1, motor5Pin2, positionPin5, targetPosition);
  }
  else if (command.startsWith("m3to")) {
    int targetAngle = command.substring(4).toInt();
    int targetPosition = map(targetAngle, mapped3Min, mapped3Max, motor3Max, motor3Min);
    moveToPosition(motor3Pin1, motor3Pin2, positionPin3, targetPosition);
    
  }
  else if (command.startsWith("m4to")) {
    int targetAngle = command.substring(4).toInt();
    int targetPosition = map(targetAngle, mapped2Min, mapped2Max, motor2Min, motor2Max);
    moveToPosition(motor2Pin1, motor2Pin2, positionPin2, targetPosition);

  }
  else if (command.startsWith("m5to")) {
    int targetAngle = command.substring(4).toInt();
    int targetPosition = map(targetAngle, mapped1Min, mapped1Max, motor1Max, motor1Min);
    moveToPositionsingle(motor1Pin1, motor1Pin2, positionPin1, targetPosition);
  }

  
}

void moveToPosition(int motorPin1, int motorPin2, int positionPin, int targetPosition) {
  for (int i = 0; i < 4; i++) { // Perform the action 3 times
    int currentPosition = analogRead(positionPin);

    while (currentPosition < targetPosition - 1 || currentPosition > targetPosition + 1) {
      if (currentPosition < targetPosition) {
        digitalWrite(motorPin1, HIGH); // Move in one direction
        digitalWrite(motorPin2, LOW);
      } else {
        digitalWrite(motorPin1, LOW); // Move in the opposite direction
        digitalWrite(motorPin2, HIGH);
      }

      currentPosition = analogRead(positionPin);
      delay(5); // Small delay to allow for movement
    }

    // Stop the motor
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);

    // Small delay between iterations (optional)
    delay(250);
  }}


void moveToPositionsingle(int motorPin1, int motorPin2, int positionPin, int targetPosition) {

    int currentPosition = analogRead(positionPin);

    while (currentPosition < targetPosition - 2 || currentPosition > targetPosition + 2) {
      if (currentPosition < targetPosition) {
        digitalWrite(motorPin1, HIGH); // Move in one direction
        digitalWrite(motorPin2, LOW);
      } else {
        digitalWrite(motorPin1, LOW); // Move in the opposite direction
        digitalWrite(motorPin2, HIGH);
      }

      currentPosition = analogRead(positionPin);
      delay(5); // Small delay to allow for movement
    }

    // Stop the motor
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);

    // Small delay between iterations (optional)
    delay(250);
}

void printMotorPositions() {
  int val=analogRead(positionPin4);
  Serial.print("m1to");
  Serial.print( map(val, motor4Min, motor4Max,mapped4Min,mapped4Max));
  Serial.print(";");
  val=analogRead(positionPin5);
  Serial.print("m2to");
  Serial.print( map(val, motor5Min, motor5Max,mapped5Min,mapped5Max));
  Serial.print(";");
  val=analogRead(positionPin3);
  Serial.print("m3to");
  Serial.print( 90-map(val, motor3Min, motor3Max,mapped3Min,mapped3Max));
  Serial.print(";");
  val=analogRead(positionPin2);
  Serial.print("m4to");
  Serial.print( map(val, motor2Min, motor2Max,mapped2Min,mapped2Max));
  Serial.print(";");
  val=analogRead(positionPin1);
  
  Serial.print("m5to");
  Serial.print( map(val, motor1Min, motor1Max,mapped1Min,mapped1Max));
  Serial.println(";");
 
}
 
