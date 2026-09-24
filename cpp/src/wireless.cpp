#include "wireless.h"
#include "gpio.h"
#include "device_manager.h"
#include "device.h"

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

void setLevel() {
    if (!server.hasArg("level"))
        server.send(400, "text/plain", String("missing param level"));
    if (!server.hasArg("deviceNum"))
        server.send(400, "text/plain", String("missing param deviceId"));

    int level = server.arg("level").toInt();
    int deviceId = server.arg("deviceId").toInt();

    DeviceManager* deviceManager = DeviceManager::getInstance();
    Device* device = deviceManager->getDevice(deviceId);

    //check if device is dimmable, send an error code if not
    //runtime polymorphism is not possible on this (RTTI disabled on esp32 to save flash)
    if (device->setLevel(level))
        server.send(200, "text/plain", String("Device " + String(deviceId) +  " set to " + String(level)));
    else
        server.send(400, "text/plain", String("Device " + String(deviceId) + "is not dimmable or failed to dim"));
}