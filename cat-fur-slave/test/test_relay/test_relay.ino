#define RELAY_ACT_0             4
#define RELAY_ACT_1             5     

void setup() {
        pinMode(RELAY_ACT_0, OUTPUT);
        pinMode(RELAY_ACT_1, OUTPUT);       

        digitalWrite(RELAY_ACT_0, LOW);
        digitalWrite(RELAY_ACT_1, HIGH);
}

void loop() {
        
}
