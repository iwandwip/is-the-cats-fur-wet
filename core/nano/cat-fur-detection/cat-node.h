#include <math.h>
#pragma once

#ifndef CAT_NODE_H
#define CAT_NODE_H

#include "Arduino.h"
#include "cat-def.h"
#include "stdint.h"

#include <Servo.h>

namespace act {

template<typename actClassPtr = uint8_t*>
struct act {
        actClassPtr actClass;
        uint8_t actPin;
        uint8_t actState;
};

typedef enum {
        CAT_RELAY_0,
        CAT_RELAY_1
} relay_index;

}

struct actuator {
        act::act<uint8_t*> relay[2];
        act::act<Servo* > servo;
};

void cat_node_init(actuator* packet);
void cat_node_loop(actuator* packet);

void cat_node_debug(actuator* packet);

#endif  // CAT_NODE_H