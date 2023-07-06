#include "sensor-module.h"
#include "output-module.h"
#include "serial-com.h"
#include "dht-sens.h"
#include "HCSR04.h"
#include "Servo.h"

#define SSR_PIN 3
#define SSR_THRESHOLD_UP 35.00
#define SSR_THRESHOLD_MID 30.00

SensorModule sensor;
SerialCom com;

float dhtValue[2];
float distValue;
int condition[5];

DigitalOut dcFanA(4);
DigitalOut dcFanB(5);
DigitalOut dcFanC(8);
DigitalOut dcFanD(9);

void setup() {
        Serial.begin(9600);
        sensor.addModule(new DHTSens(2));
        sensor.addModule(new Sonar(6, 7));
        sensor.init();
        pinMode(SSR_PIN, OUTPUT);
}

void loop() {
        sensor.update(sensorRoutine);
        com.clearData();
        com.addData(dhtValue[0], " ");
        com.addData(dhtValue[1], " ");
        com.addData(distValue, " ");
        for (uint8_t i = 0; i < 4; i++) {
                com.addData(condition[i], " ");
        }
        com.sendData(1000);
        com.receive(onReceive);

        if (condition[0] == 0) {
                if (dhtValue[0] < SSR_THRESHOLD_MID) {
                        analogWrite(SSR_PIN, 255);
                } else if (dhtValue[0] >= SSR_THRESHOLD_MID && dhtValue[0] < SSR_THRESHOLD_UP) {
                        analogWrite(SSR_PIN, 128);
                } else {
                        analogWrite(SSR_PIN, 0);
                }
        } else {
                analogWrite(SSR_PIN, 0);
        }

        (condition[1] == 1) ? dcFanA.on() : dcFanA.off();
        (condition[2] == 1) ? dcFanB.on() : dcFanB.off();
        (condition[3] == 1) ? dcFanC.on() : dcFanC.off();
        (condition[4] == 1) ? dcFanD.on() : dcFanD.off();
}

void sensorRoutine() {
        sensor.getModule(0)->getSensorValue(dhtValue);
        sensor.getModule(1)->getSensorValue(&distValue);
}

void onReceive(String data) {
        for (uint8_t i = 0; i < 5; i++) {
                condition[i] = (int)com.getData(data, i);
        }
}