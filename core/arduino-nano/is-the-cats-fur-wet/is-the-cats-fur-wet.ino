#include "sensor-module.h"
#include "output-module.h"
#include "serial-com.h"
#include "dht-sens.h"
#include "HCSR04.h"
#include "Servo.h"

// macros
#define DHT_SENS_PIN 2
#define SERVO_ACT_PIN 3
#define RELAY_SATU_PIN 4
#define RELAY_DUA_PIN 5
#define ULT_ECHO_PIN 8
#define ULT_TRIG_PIN 9

SensorModule sensor;
SerialCom com;

float dhtValue[2];
float distValue;
int stateCatFur;

Servo servo;
DigitalOut relaySatu, relayDua;

void setup() {
        Serial.begin(9600);
        servo.attach(SERVO_ACT_PIN);
        relaySatu.setPins(RELAY_SATU_PIN, true);
        relayDua.setPins(RELAY_DUA_PIN, true);

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
        com.sendData(1000);
        com.receive(onReceive);

        if (stateCatFur) {
                relaySatu.on();
                relayDua.on();
        } else {
                relaySatu.off();
                relayDua.off();
        }
}

void sensorRoutine() {
        sensor.getModule(0)->getSensorValue(dhtValue);
        sensor.getModule(1)->getSensorValue(&distValue);
}

void onReceive(String data) {
        stateCatFur = (int)com.getData(data, 0);
}