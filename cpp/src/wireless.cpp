#include "wireless.h"
#include "gpio.h"
#include "device_manager.h"
#include "device.h"

void enableLED() {
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

void disableLED() {
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


void setLevel() {
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