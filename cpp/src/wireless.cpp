#include "wireless.h"
#include "gpio.h"

//toggle
void toggleLED() {
    if (!server.hasArg("gpio")) {
        server.send(400, "text/plain", "Missing gpio parameter");
        return;
    }

    int gpio = server.arg("gpio").toInt();

    std::string ledStatus = std::to_string(togglePin(gpio));
    Serial.println("LED API");
    server.send(200, "text/plain", ledStatus.c_str());
}

void enableLED() {
    //enable all connected devices
    if (!server.hasArg("pin")) {
        for (uint8_t pin = 12; pin <= 14; pin++) {
            digitalWrite(pin, true);
        }

        Serial.println("All devices enabled");
        server.send(200, "text/plain", String("all"));
        return;
    }

    //enable one specific device
    int pin_number = server.arg("pin").toInt();

    digitalWrite(pin_number, true);

    Serial.println("Pin " + String(pin_number) + " enabled");
    server.send(200, "text/plain", String(pin_number));
}

void disableLED() {
    //disable all connected devices
    if (!server.hasArg("pin")) {
        for (uint8_t pin = 12; pin <= 14; pin++) {
            digitalWrite(pin, false);
        }

        Serial.println("All devices disabled");
        server.send(200, "text/plain", String("all"));
        return;
    }

    //enable one specific device
    int pin_number = server.arg("pin").toInt();

    digitalWrite(pin_number, false);

    Serial.println("Pin " + String(pin_number) + " disabled");
    server.send(200, "text/plain", String(pin_number));
}