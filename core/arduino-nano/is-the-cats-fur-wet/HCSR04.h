/*
 *  HCSR04.h
 *
 *  HCSR04 sensor lib
 *  Created on: 2023. 4. 3
 */

#pragma once

#ifndef HCSR04_H
#define HCSR04_H

#include "Arduino.h"
#include "sensor-module.h"
#include "stdint.h"

#include "NewPing.h"

class Sonar : public BaseSens {
      private:
        NewPing* sonar;
        uint8_t echoPin;
        uint8_t triggPin;
        float* distance;

        uint32_t update_tm;
        uint32_t debug_tm;
        uint32_t* cal_tm;

        bool isCalibrate;

        float getSensorAverage(float sensorValue, int numReadings = 10);
        float lowPassFilter(float input, float output, float alpha);
      public:
        Sonar(bool enableCalibrate = false);
        Sonar(uint8_t echo, uint8_t trigg, bool enableCalibrate = false);
        ~Sonar();

        void init() override;
        void update() override;
        void debug() override;
        void calibrate() override;
        void getSensorValue(float* value) override;
        void getSensorValue(int* value) override;
        void count() override;
        void reset() override;

        float getValue(sens_ret_index_t c = SENS_RET_ACT_DATA);
        void setPins(uint8_t echo, uint8_t trigg);
};

#endif  // HCSR04_H