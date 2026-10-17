#include "wireless.h"
#include "device_manager.h"
#include "device.h"

#include <sstream>
#include <ArduinoJson.h>

static std::string deviceIdsToString(const std::vector<uint8_t>& deviceIds) {
    std::string result;
    for (const auto& id : deviceIds) {
        if (!result.empty()) {
            result += ", ";
        }

        result += std::to_string(id);
    }

    return result;
}

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

    if (deserializeJson(doc, json)) {
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

    server.send(200, "text/plain", "Devices added successfully");

    std::ostringstream oss;
    oss << *deviceManager;
    Serial.println(oss.str().c_str());
}

void enableAllDevices() {
    DeviceManager* deviceManager = DeviceManager::getInstance();

    std::vector<uint8_t> errors = {};
    for (const auto& [deviceId, device] : deviceManager->getAllDevices()) {
        if (!device->setState(true)) {
            errors.push_back(deviceId);
        }
    }

    if (!errors.empty()) {
        server.send(200, "text/plain", "Devices: " + String(deviceIdsToString(errors).c_str()) + " could not be enabled");
    }
    else {
        server.send(200, "text/plain", "All devices enabled");
    }
}

void enableDevice() {
    if (!server.hasArg("deviceId")) {
        server.send(400, "text/plain", "missing param");
        return;
    }

    String param = server.arg("deviceId");

    //enable all devices
    if (param == "all") {
        enableAllDevices();
        return;
    }

    //enable one specific device
    int deviceId = param.toInt();
    DeviceManager* deviceManager = DeviceManager::getInstance();
    Device* device = deviceManager->getDevice(deviceId);

    if (!device) {
        server.send(400, "text/plain", "Device " + String(deviceId) + " could not be found");
        return;
    }

    if (device->setState(true))
        server.send(200, "text/plain", "Device " + String(deviceId) +  " enabled");
    else
        server.send(400, "text/plain", "Device " + String(deviceId) + " failed to enable");
}

void disableAllDevices() {
    DeviceManager* deviceManager = DeviceManager::getInstance();

    std::vector<uint8_t> errors = {};
    for (const auto& [deviceId, device] : deviceManager->getAllDevices()) {
        if (!device->setState(false)) {
            errors.push_back(deviceId);
        }
    }

    if (!errors.empty()) {
        server.send(200, "text/plain", "Devices: " + String(deviceIdsToString(errors).c_str()) + " could not be disabled");
    }
    else {
        server.send(200, "text/plain", "All devices disabled");
    }
}

void disableDevice() {
    //disable all connected devices
    if (!server.hasArg("deviceId")) {
        server.send(400, "text/plain", "missing param");
        return;
    }

    String param = server.arg("deviceId");

    //disable all devices
    if (param == "all") {
        disableAllDevices();
        return;
    }

    //disable one specific device
    int deviceId = param.toInt();
    DeviceManager* deviceManager = DeviceManager::getInstance();
    Device* device = deviceManager->getDevice(deviceId);

    //disable one specific device
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