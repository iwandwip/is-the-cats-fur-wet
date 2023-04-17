#include <Servo.h>
#include "NewPing.h"

#define SERVO_ACT_PIN 3
#define RELAY_ACT_0 4
#define RELAY_ACT_1 5

#define ULTRA_ECHO 9
#define ULTRA_TRIGG 8

Servo myservo;
NewPing sonar(ULTRA_ECHO, ULTRA_TRIGG, 200);

int pos = 0;

void setup() {
        Serial.begin(9600);
        myservo.attach(SERVO_ACT_PIN);
}

void loop() {
        for (pos = 0; pos <= 180; pos += 1) {
                myservo.write(pos);
                delay(15);
        }
        for (pos = 180; pos >= 0; pos -= 1) {
                myservo.write(pos);
                delay(15);
        }
        Serial.println(sonar.ping_cm());
}
