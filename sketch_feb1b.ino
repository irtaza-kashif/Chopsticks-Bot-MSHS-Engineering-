#include <Servo.h>
#define SERVOS 10
Servo myservo[SERVOS];

int servo_pins[SERVOS] = {2,3,4,5,6,7,8,9,10,11};
int closed_pos = 0;
int open_pos = 90;
int rCount = 0;
int lCount = 0;

void setup() {
  // It will be recieving data in the form of "2,3", "4,4", "TRANSFER,2,3", "RIGHT,LEFT"
  for(int i = 0; i < SERVOS; i++) {
    myservo[i].attach(servo_pins[i]);
    myservo[i].write(closed_pos);
    delay(250);
  }

  setHands(lCount, rCount);

  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  //Waiting for a change of bits in information recieved
  if (Serial.available() > 0) {
    String command = Serial.readString();

    // Determining what the command / input is 
    if (isDigit(command.charAt(0))) {
      lCount = command.charAt(0) - '0';
      rCount = command.charAt(2) - '0';

      setHands(lCount, rCount);
    } else {
      if (command.charAt(0) == 'T') {
        // TODO add wrist movement

        lCount = command.charAt(9) - '0';
        rCount = command.charAt(11) - '0';
        setHands(lCount, rCount);
      } else if (command.charAt(0) == 'L') {
          if (commmand.charAt(5) == 'L'){

          }
          if (commmand.charAt(5) == 'R'){

          }

        } 
      
        else if (command.charAt(0) == 'R') {
          if (commmand.charAt(6) == 'L'){

          }
          if (commmand.charAt(6) == 'R'){

          }
        }

      
    }
  }
}

// This displays the fingers appropraitely to their hands' number
void setHands(int lCount, int rCount) {

  //Right hand
  for(int i = 0; i<rCount; i++){
    myservo[i].write(open_pos);
    delay(250);
  }
  for(int i = 3; i>=rCount; i--){
    myservo[i].write(closed_pos);
    delay(250);
  }

  //Left hand
  for(int i = 4; i<lCount+4; i++){
    myservo[i].write(open_pos);
    delay(250);
  }
  for(int i = 7; i>=lCount+4; i--){
    myservo[i].write(closed_pos);
    delay(250);
  }
}