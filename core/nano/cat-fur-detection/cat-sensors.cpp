#include "HardwareSerial.h"
#include "Arduino.h"
#include "cat-sensors.h"
#include "cat-def.h"

#define DHTTYPE DHT22
#define DHT_SAMPLING_TIME 1000
#define DHT_FILTER_KF 8

#define ULTRA_MAX_DISTANCE 200
#define ULTRA_SAMPLING_TIME 300
#define ULTRA_FILTER_KF 8

#define WINDOW_SIZE 5
#define NO_OFFSET 0

// internal function
float movingAverageFilter(float newValue);
float gaussianFilter(float sensorValue);

void cat_sensors_init(sensors* packet) {
        packet->ult_data.sensorClass = new NewPing(ULTRA_ECHO, ULTRA_TRIGG, 200);
        packet->dht_data[0].sensorClass = new DHT(DHT22_PIN, DHTTYPE);
        packet->dht_data[0].sensorClass->begin();
}

void cat_sensors_loop(sensors* packet) {
        static uint32_t sens_tmr[2];
        packet->dht_data[TEMPERATURE].sensorOffset = NO_OFFSET;
        packet->dht_data[HUMIDITY].sensorOffset = NO_OFFSET;

        if (millis() - sens_tmr[TEMPERATURE] >= DHT_SAMPLING_TIME) {
                packet->dht_data[TEMPERATURE].rawSensorData = packet->dht_data[0].sensorClass->readTemperature();
                packet->dht_data[HUMIDITY].rawSensorData = packet->dht_data[0].sensorClass->readHumidity();

                for (uint8_t i = 0; i < 2; i++) {
                        packet->dht_data[i].sensorData = packet->dht_data[i].rawSensorData + (packet->dht_data[i].rawSensorData * DHT_FILTER_KF);
                        packet->dht_data[i].sensorData /= DHT_FILTER_KF + 1;
                        packet->dht_data[i].sensorAvg = movingAverageFilter(packet->dht_data[i].sensorData);
                        packet->dht_data[i].sensorFiltered = gaussianFilter(packet->dht_data[i].sensorData);
                }
                sens_tmr[TEMPERATURE] = millis();
        }
        if (millis() - sens_tmr[1] >= ULTRA_SAMPLING_TIME) {
                packet->ult_data.rawSensorData = packet->ult_data.sensorClass->ping_cm();
                packet->ult_data.sensorData = packet->ult_data.rawSensorData + (packet->ult_data.rawSensorData * ULTRA_FILTER_KF);
                packet->ult_data.sensorData /= ULTRA_FILTER_KF + 1;
                packet->ult_data.sensorAvg = movingAverageFilter(packet->ult_data.sensorData);
                packet->ult_data.sensorFiltered = gaussianFilter(packet->ult_data.sensorData);
                sens_tmr[1] = millis();
        }
}

void cat_sensors_debug(sensors* packet) {
        static uint32_t debug_tm;
        if (millis() - debug_tm >= 30) {
                Serial.print("Temp: ");
                Serial.print(packet->dht_data[TEMPERATURE].sensorData);
                Serial.print("| Temp: ");
                Serial.print(packet->dht_data[HUMIDITY].sensorData);
                Serial.print("| Dist: ");
                Serial.print(packet->ult_data.sensorData);
                Serial.println();
                debug_tm = millis();
        }
}

float movingAverageFilter(float newValue) {
        static float window[WINDOW_SIZE];
        static int index = 0;
        static float sum = 0;

        sum -= window[index];
        sum += newValue;
        window[index] = newValue;
        index = (index + 1) % WINDOW_SIZE;

        return sum / WINDOW_SIZE;
}

float gaussianFilter(float sensorValue) {
        const float filterWeight[7] = { 0.06136, 0.24477, 0.38774, 0.24477, 0.06136 };
        const int filterLength = 5;

        static float sensorBuffer[5];
        static int index = 0;

        float filteredValue = 0.0;
        sensorBuffer[index] = sensorValue;
        index++;

        if (index >= filterLength) index = 0;
        for (int i = 0; i < filterLength; i++) {
                int bufferIndex = (index + i) % filterLength;
                filteredValue += filterWeight[i] * sensorBuffer[bufferIndex];
        }
        return filteredValue;
}