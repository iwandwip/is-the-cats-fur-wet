#include "cat-sensors.h"
#include "cat-node.h"

actuator acts;
sensors sensor;

void setup() {
        Serial.begin(9600);
        cat_sensors_init(&sensor);
        cat_node_init(&acts);
}

void loop() {
        cat_sensors_loop(&sensor);
        cat_sensors_debug(&sensor);

        cat_node_loop(&acts);
}
