#include "wireless.h"
#include "device_manager.h"
#include "device.h"

#include <sstream>
#include <ArduinoJson.h>

void setupDevices() {
    //Clear existing devices
    DeviceManager* deviceManager = DeviceManager::getInstance();
    deviceManager->clearDevices();

    if (!server.hasArg("plain")) {
        server.send(400, "text/plain", "Missing JSON body");
        return;
    }

    String json = server.arg("plain");

    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, json);

    if (error) {
        server.send(400, "text/plain", "Invalid JSON");
        return;
    }


    JsonArray devices = doc["devices"].as<JsonArray>();

    uint8_t count = 0;
    for (auto device : devices) {
        bool isDimmable = device["dimmable"];
        std::string nickname = device["nickname"] | ""; //empty string if nickname is not there

        if (isDimmable) {
            uint8_t zeroCrossPin = device["zeroCrossPin"] | 0;
            uint8_t dimmerPin = device["dimmerPin"] | 0;

            if (!zeroCrossPin || !dimmerPin) {
                Serial.println("Device number " + String(count) + " has invalid data");
                server.send(400, "text/plain", "Invalid device data");
                return;
            }

            Device* newDevice = new Dimmable(zeroCrossPin, dimmerPin, nickname);

            if (!deviceManager->addDevice(newDevice)) {
                delete newDevice;
                server.send(400, "text/plain", "Something went wrong with adding device " + String(count));
                return;
            }
        }
        else {
            uint8_t togglePin = device["togglePin"] | 0;

            if (!togglePin) {
                Serial.println("Device number " + String(count) + " has invalid data");
                server.send(400, "text/plain", "Invalid device data");
                return;
            }

            Device* newDevice = new Toggleable(togglePin, nickname);

            if (!deviceManager->addDevice(newDevice)) {
                delete newDevice;
                server.send(400, "text/plain", "Something went wrong with adding device " + String(count));
                return;
            }
        }

        count++;
    }

    server.send(200, "text/plain", String("Devices added successfully"));

    std::ostringstream oss;
    oss << *deviceManager;
    Serial.println(oss.str().c_str());
}

void enableDevice() {
    //enable all connected devices
    if (!server.hasArg("deviceId")) {
        server.send(400, "text/plain", String("missing param"));
        return;
    }

    //enable one specific device
    int deviceId = server.arg("deviceId").toInt();

    DeviceManager* deviceManager = DeviceManager::getInstance();
    Device* device = deviceManager->getDevice(deviceId);

    if (!device) {
        server.send(400, "text/plain", String("Device " + String(deviceId) + " could not be found"));
        return;
    }

    if (device->setState(true))
        server.send(200, "text/plain", String("Device " + String(deviceId) +  " enabled"));
    else
        server.send(400, "text/plain", String("Device " + String(deviceId) + " failed to enable"));
}

void disableDevice() {
    //disable all connected devices
    if (!server.hasArg("deviceId")) {
        server.send(400, "text/plain", String("missing param"));
        return;
    }

    //disable one specific device
    int deviceId = server.arg("deviceId").toInt();

    DeviceManager* deviceManager = DeviceManager::getInstance();
    Device* device = deviceManager->getDevice(deviceId);

    if (!device) {
        server.send(400, "text/plain", String("Device " + String(deviceId) + " could not be found"));
        return;
    }

    if (device->setState(false))
        server.send(200, "text/plain", String("Device " + String(deviceId) +  " disabled"));
    else
        server.send(400, "text/plain", String("Device " + String(deviceId) + " failed to disable"));
}


void setDeviceLevel() {
    if (!server.hasArg("level"))
        server.send(400, "text/plain", String("missing param level"));
    if (!server.hasArg("deviceId"))
        server.send(400, "text/plain", String("missing param deviceId"));

    int level = server.arg("level").toInt();
    int deviceId = server.arg("deviceId").toInt();

    DeviceManager* deviceManager = DeviceManager::getInstance();
    Device* device = deviceManager->getDevice(deviceId);

    if (!device) {
        server.send(400, "text/plain", String("Device " + String(deviceId) + " could not be found"));
        return;
    }

    //check if device is dimmable, send an error code if not
    if (device->setLevel(level))
        server.send(200, "text/plain", String("Device " + String(deviceId) +  " set to " + String(level)));
    else
        server.send(400, "text/plain", String("Device " + String(deviceId) + "is not dimmable or failed to dim"));
}