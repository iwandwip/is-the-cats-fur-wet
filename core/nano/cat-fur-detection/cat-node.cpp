#include "Arduino.h"
#include "cat-node.h"

void cat_node_init(actuator* packet) {
        packet->relay[act::CAT_RELAY_0].actPin = RELAY_ACT_0;
        packet->relay[act::CAT_RELAY_1].actPin = RELAY_ACT_1;
        packet->servo.actClass = new Servo;
        packet->servo.actClass->attach(SERVO_ACT_PIN);

        for (uint8_t i = 0; i < 2; i++) {
                pinMode(packet->relay[i].actPin, OUTPUT);
        }

        digitalWrite(packet->relay[act::CAT_RELAY_0].actPin, LOW);
        digitalWrite(packet->relay[act::CAT_RELAY_1].actPin, LOW);

        packet->servo.actClass->write(180);
}

void cat_node_loop(actuator* packet) {
}

void cat_node_debug(actuator* packet) {
}