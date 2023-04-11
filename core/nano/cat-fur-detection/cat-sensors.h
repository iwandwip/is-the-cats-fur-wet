#pragma once

#ifndef CAT_SENSORS_H
#define CAT_SENSORS_H

#include "Arduino.h"
#include "stdint.h"

#include "NewPing.h"
#include "DHT.h"

namespace data {

template<typename dTypes, typename cNamePtr = uint8_t*>
struct sens_data {
        cNamePtr sensorClass;
        dTypes rawSensorData;
        dTypes sensorFiltered;
        dTypes sensorOffset;
        dTypes sensorData;
        dTypes sensorAvg;
};

}

typedef enum {
        TEMPERATURE,
        HUMIDITY
} dht_index;

struct sensors {
        data::sens_data<uint16_t, NewPing*> ult_data;
        data::sens_data<float, DHT*> dht_data[2];
};

void cat_sensors_init(sensors* packet);
void cat_sensors_loop(sensors* packet);

void cat_sensors_debug(sensors* packet);

#endif  // CAT_SENSORS_H