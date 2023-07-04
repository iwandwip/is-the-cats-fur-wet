#include "sensor-module.h"
#include "output-module.h"
#include "serial-com.h"
#include "dht-sens.h"
#include "HCSR04.h"
#include "Servo.h"

// macros
#define DHT_SENS_PIN 2
#define RELAY_SATU_PIN 3
#define RELAY_DUA_PIN 4
#define RELAY_TIGA_PIN 5
#define ULT_ECHO_PIN 8
#define ULT_TRIG_PIN 9

SensorModule sensor;
SerialCom com;

float dhtValue[2];
float distValue;
int condition[4];

DigitalOut dcFanA(3), dcFanB(4), dcFanC(5);

void setup() {
        Serial.begin(9600);

        sensor.addModule(new DHTSens(DHT_SENS_PIN));
        sensor.addModule(new Sonar(ULT_ECHO_PIN, ULT_TRIG_PIN));
        sensor.init();
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

        // (condition[1]) ? dcFanA.on() : dcFanA.off();
        // (condition[2]) ? dcFanB.on() : dcFanB.off();
        // (condition[3]) ? dcFanC.on() : dcFanC.off();

        if (condition[1]) {
                dcFanA.on();
        } else {
                dcFanA.off();
        }
        if (condition[2]) {
                dcFanB.on();
        } else {
                dcFanB.off();
        }
        if (condition[3]) {
                dcFanC.on();
        } else {
                dcFanC.off();
        }
}

void sensorRoutine() {
        sensor.getModule(0)->getSensorValue(dhtValue);
        sensor.getModule(1)->getSensorValue(&distValue);
}

void onReceive(String data) {
        for (uint8_t i = 0; i < 4; i++) {
                condition[i] = (int)com.getData(data, i);
        }
}