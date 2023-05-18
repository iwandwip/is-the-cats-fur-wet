/*
 *  dht-sens.cpp
 *
 *  dht sensor c
 *  Created on: 2023. 4. 3
 */

#include "dht-sens.h"
#include "Arduino.h"
#include "SimpleKalmanFilter.h"

#define SENSOR_FILTER_KF 8

DHTSens::DHTSens()
  : sensorPin(A0) {
        isCalibrate = false;
        tempHumValue = (isCalibrate) ? new float[2][SENS_RET_TOTAL_DATA] : new float[2];
        if (isCalibrate) cal_tm = new uint32_t;
}

DHTSens::DHTSens(uint8_t __pin, bool enableCalibrate) {
        this->sensorPin = __pin;
        isCalibrate = enableCalibrate;
        tempHumValue = (isCalibrate) ? new float[2][SENS_RET_TOTAL_DATA] : new float[2];
        if (isCalibrate) cal_tm = new uint32_t;
}

DHTSens::~DHTSens() {
        delete this;
}

void DHTSens::init() {
        sensorClass = new DHT(sensorPin, DHT22);
        sensorClass->begin();
}

void DHTSens::update() {
        if (millis() - update_tm >= 500) {
                if (!isCalibrate) {
                        tempHumValue[0] = sensorClass->readTemperature();
                        tempHumValue[1] = sensorClass->readHumidity();

                        for (uint8_t i = 0; i < 2; i++) {
                                tempHumValue[i] = tempHumValue[i] + (tempHumValue[i] * SENSOR_FILTER_KF);
                                tempHumValue[i] /= SENSOR_FILTER_KF + 1;
                        }
                } else {
                        SimpleKalmanFilter* sonarKf = new SimpleKalmanFilter(2, 2, 0.01);
                        // tempHumValue[0][SENS_RET_RAW_DATA] = sensorClass->readTemperature();
                        // tempHumValue[1][SENS_RET_RAW_DATA] = sensorClass->readHumidity();

                        // for (uint8_t i = 0; i < 2; i++) {
                        //         tempHumValue[i][SENS_RET_ACT_DATA] = tempHumValue[i][SENS_RET_RAW_DATA] + (tempHumValue[i][SENS_RET_RAW_DATA] * SENSOR_FILTER_KF);
                        //         tempHumValue[i][SENS_RET_ACT_DATA] /= SENSOR_FILTER_KF + 1;

                        //         tempHumValue[i][SENS_RET_AVG_DATA] = getSensorAverage(tempHumValue[i][SENS_RET_ACT_DATA]);
                        //         tempHumValue[i][SENS_RET_FILTERED_DATA] = lowPassFilter(tempHumValue[i][SENS_RET_ACT_DATA], tempHumValue[i][SENS_RET_FILTERED_DATA], 0.1);
                        //         tempHumValue[i][SENS_RET_FILTERED_DATA] = sonarKf->updateEstimate(tempHumValue[i][SENS_RET_ACT_DATA]);
                        // }
                        delete sonarKf;
                }

                update_tm = millis();
        }
}

void DHTSens::debug() {
        if (millis() - debug_tm >= 500) {
                if (isCalibrate) return;
                Serial.print("| tempValueRaw: ");
                Serial.print(tempHumValue[0]);
                Serial.print("| humidValueRaw: ");
                Serial.print(tempHumValue[1]);
                Serial.println();
                debug_tm = millis();
        }
}

void DHTSens::calibrate() {
        if (millis() - *cal_tm >= 500) {
                if (!isCalibrate) return;
                Serial.print("| tempHumValueRaw: ");
                Serial.print(tempHumValue[SENS_RET_RAW_DATA]);
                Serial.print("| tempHumValueAct: ");
                Serial.print(tempHumValue[SENS_RET_ACT_DATA]);
                Serial.print("| tempHumValueAvg: ");
                Serial.print(tempHumValue[SENS_RET_AVG_DATA]);
                Serial.print("| tempHumValueFiltered: ");
                Serial.print(tempHumValue[SENS_RET_FILTERED_DATA]);
                Serial.println();
                *cal_tm = millis();
        }
}

void DHTSens::getSensorValue(float* value) {
        value[0] = tempHumValue[0];
        value[1] = tempHumValue[1];
}

void DHTSens::getSensorValue(int* value) {
}

void DHTSens::count() {
}

void DHTSens::reset() {
}

float DHTSens::getValue(sens_ret_index_t c) {
        if (!isCalibrate) return *tempHumValue;
        return tempHumValue[c];
}

void DHTSens::setPins(uint8_t __pin) {
        this->sensorPin = __pin;
}

float DHTSens::getSensorAverage(float sensorValue, int numReadings) {
        float sensorSum = 0;
        for (int i = 0; i < numReadings; i++) {
                sensorSum += sensorValue;
        }
        return sensorSum / (float)numReadings;
}

float DHTSens::lowPassFilter(float input, float output, float alpha) {
        output = (alpha * input) + ((1.0 - alpha) * output);
        return output;
}