/* modified 12 Feb 2020
 by Asude Aydin

 Refer to https://www.arduino.cc/en/tutorial/sweep
 https://cdn.sparkfun.com/assets/learn_tutorials/6/7/6/PiZero_1.pdf
 https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
 https://oscarliang.com/raspberry-pi-arduino-connected-i2c/
 */

#include <Wire.h>
#include <Servo.h>

Servo myservo; // create servo object to control a servo

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;
int pos = 0 ;

void setup() {

  myservo.attach(9); // attaches the servo on pin 9 to the servo object
  pinMode(13, OUTPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
}
  
void loop() {
delay(100);
}

// callback for received data
void receiveData(int byteCount){
  
  while(Wire.available()){
    number = Wire.read();
    // Serial.print("data received: ");
    // Serial.println(number);
    
    if (number == 1){
    
      myservo.write(0); // servo takes position 0 angle 
      delay(50); // delay for 1 sec
    }
    
      // to give small amount of food
    if (number == 2){
    
      myservo.write(50); // servo takes position 50 angle 
      delay(50); // delay for 1 sec
    }
    
      //to give medium amount of food
    
    if (number == 3){
    
      myservo.write(60); // servo takes position 60 angle 
      delay(50); // delay for 1 sec
    }
    
        //to give large amount of food
    
    if (number == 4){
    
      myservo.write(70); // servo takes position 60 angle 
      delay(50); // delay for 1 sec
    }

    // Toggles led
    
    if (number == 5){
    
      if (state == 0){
      digitalWrite(13, HIGH); // set the LED on
      state = 1;
      }
      else{
      digitalWrite(13, LOW); // set the LED off
      state = 0;
        }
    }
  }
}

// callback for sending data
void sendData(){
  Wire.write(number);
}
