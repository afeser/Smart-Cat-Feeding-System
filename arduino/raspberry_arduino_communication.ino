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

int analogPinrasp = A4; // raspberry pil
int analogPinmotor = A5; // motor pil biri

int voltagerasp = 0;
int voltagemotor = 0;

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
                                      
    if (0 < number < 181) {
      Serial.print("data received: ");
      Serial.println(number);                          
      myservo.write(number-1);    // servo 0-180 derece arası calısıyor.
      delay(50);
    }
    
    // Toggles led
    
    if (number == 181){
    
      if (state == 0){
      digitalWrite(13, HIGH); // set the LED on
      state = 1;
      }
      else{
      digitalWrite(13, LOW); // set the LED off
      state = 0;
        }
    }     
                                     
    if (number == 182) {
                                
      voltagerasp = analogRead(analogPinrasp);
      float number = voltagerasp * (5.0 / 1023.0);
      delay(50);
    }

    if (number == 183) {
                                
      voltagemotor = analogRead(analogPinmotor);
      float number = voltagemotor * (5.0 / 1023.0);
      delay(50);
    }

    
  }
}

// callback for sending data
void sendData(){
  Wire.write(number);
}
